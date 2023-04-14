rm(list = ls())
setwd("D:/ftp/jackraymond/")
'%notin%' = Negate('%in%')
################################################
library(limma)
library(minfi)
library(sesame)
library(IlluminaHumanMethylationEPICanno.ilm10b4.hg19)
set.seed(123)
################# READ BETAS + PDATA ###################################

## read in the normalized betas values. rows are CPGs and columns are IDAT samples IDs
# betas_normalized = read.csv("C:/Users/jack/PycharmProjects/TruDiagnostic/Covariate Models/Blood Type/Data/BetaMatrix_Funnorm_RCP_normalized_betas_1642081709.csv")
betas_normalized = read.csv("D:/ftp/jackraymond/ToddO_Clinic_betas.GMQN.csv")

rownames(betas_normalized) = betas_normalized[,1]
betas_normalized = betas_normalized[,-c(1)]
colnames(betas_normalized) = sub("X","",colnames(betas_normalized))
# betas_normalized = t(betas_normalized)
print(betas_normalized[1:10, 1:10])
# print(betas_normalized_[1:10, 1:10])


## Read in PData 
## read in the pdata file from CSV. Note that this will be different based on experiment. 
# pdata = read.csv("C:/Users/jack/PycharmProjects/TruDiagnostic/Covariate Models/Association/PopulationData_GladdenLongevity.csv")[,c(1:15,39)]
pdata = read.csv("D:/ftp/jackraymond/ToddsPopData.csv")

colnames(pdata)[1] = "Patient.ID"

## Filter pdata based on samples that are in the normalized beta values
pdata = pdata[order(pdata$Patient.ID),]
#remove = pdata[which(pdata$Dropped.Out. == "Yes"),]$PatientIdentifier
#pdata = pdata[which(pdata$PatientIdentifier %notin% remove),]
print(pdata)

## Filter normalized beta values on samples that are in pData. 
betas_normalized = betas_normalized[,which(colnames(betas_normalized)%in%pdata$Patient.ID)]
print(betas_normalized[1:10, 1:10])
betas_normalized = betas_normalized[,order(colnames(betas_normalized))]
m_values = BetaValueToMValue(betas_normalized)

##### READ IN EPIC ANNOTATION FILE #####
EPIC_annot_full = getAnnotation(IlluminaHumanMethylationEPICanno.ilm10b4.hg19)
print(EPIC_annot_full)
EPIC_annot_full_out = EPIC_annot_full[,c(1,2,2)]
rownames(EPIC_annot_full_out) = NULL
#colnames(EPIC_annot_full_out) = NULL
#write.table(EPIC_annot_full_out,"EPIC_array_background.bed",col.names = FALSE, row.names = TRUE)

################ DIFFERENTIALLY METHYLATED CpGs ################################
# Start running Differential methylation based on pairwise comparisons (e.g., 6 v 0, 3 v 0, 6 v 3)
############ Limma to identify DMLs between trials of blood, with batch as covariates ##################
time = as.factor(pdata$Test)
batch = pdata$Beadchip
print(time)

des = model.matrix(~0 + time)
print(des)
rownames(des) = colnames(m_values)
fit = lmFit(m_values, des)
cont = makeContrasts(time1 - time0, 
                     levels = des)
fit2 = contrasts.fit(fit, cont)
fit2_ebays = eBayes(fit2)
summary(decideTests(fit2_ebays))
res = topTable(fit2_ebays, adjust.method="fdr",number=nrow(m_values))
res = res[order(abs(res$logFC),decreasing = TRUE),]
hist(res$P.Value,main="Compare TruAge Test 1 vs 2",xlab="Unadjusted P values",col="cornsilk2")

res$geneID = EPIC_annot_full[match(rownames(res),rownames(EPIC_annot_full)),22]
res$gen.chr = EPIC_annot_full[match(rownames(res),rownames(EPIC_annot_full)),1]
res$gen.start = EPIC_annot_full[match(rownames(res),rownames(EPIC_annot_full)),2]
res$gen.end = EPIC_annot_full[match(rownames(res),rownames(EPIC_annot_full)),2]
res$diffMeth = "no"
res$diffMeth[res$adj.P.Val < 0.05 & res$logFC > 0] = "Hyper"
res$diffMeth[res$adj.P.Val < 0.05 & res$logFC < -0] = "Hypo"

# Write out DML results 
#res_sig = res[which(res$adj.P.Val < 0.05), ]
res_sig = res[which(res$adj.P.Val < 0.05), ]

res$LogPval =  log10(res$P.Value)*-1
nres = order(res$LogPval)
topIndices = nres[(length(nres)-15):length(nres)]
cpgs = row.names(res)[topIndices]
cpgs_vals = data.frame(res[cpgs, 'LogPval'])
row.names(cpgs_vals) <- cpgs
colnames(cpgs_vals) <- 'logFC'

semi_sig = res[which(res$P.Val < 0.05), ]
print(row.names(semi_sig))
other_significant = semi_sig[which(abs(semi_sig$logFC) > abs(20*mean(semi_sig$logFC))),]

print(cpgs_vals)
new_cpgs = row.names(other_significant)
new_df = data.frame(other_significant$logFC)
print(new_df)
print(cpgs_vals)
row.names(new_df) = new_cpgs
colnames(new_df) <- 'logFC'

print(new_df)
for(r_name in row.names(new_df)){
  r_vals = data.frame(new_df[r_name,])
  colnames(r_vals) = 'logFC'
  row.names(r_vals) = r_name
  if(!(r_name %in% row.names(cpgs_vals))){
    cpgs_vals = rbind(cpgs_vals, r_vals)
  }
}
  
print(cpgs_vals)
write.table(cpgs_vals, "ToddSignificantCpGsDMR-DML.csv", col.names = TRUE, row.names = TRUE, sep = '\t')

plot(res$logFC, res$LogPval, main='Methylation Change vs. Statistical Significance', xlab='Log2 of Fold Change', ylab='Log10 of Unadjusted P-value')

write.table(res_sig, "Todd1v2_DML_GlobalAnalysis_Significant_results.txt", col.names = TRUE, row.names = TRUE, sep = '\t')

write.table(res, "Todd1v2_DML_GlobalAnalysis_results.txt", col.names = TRUE, row.names = TRUE, sep = '\t')

# Bed files for GREAT analysis
res_sig_bed = na.omit(res_sig[which(res_sig$logFC > 0),c(8,9,10),])
res_sig_bed$name = rownames(res_sig_bed)
rownames(res_sig_bed) = NULL
colnames(res_sig_bed) = NULL
write.table(res_sig_bed, "Todd1v2_DML_HyperMethylated_GREATout.bed",col.names = FALSE, row.names = FALSE, sep = '\t')

res_sig_bed = na.omit(res_sig[which(res_sig$logFC < -0),c(8,9,10),])
res_sig_bed$name = rownames(res_sig_bed)
rownames(res_sig_bed) = NULL
colnames(res_sig_bed) = NULL
write.table(res_sig_bed, "Todd1v2_DML_HypoMethylated_GREATout.bed",col.names = FALSE, row.names = FALSE, sep = '\t')

print(res$P.Value)
res_filtered = res[res$P.Value<.05, ]
print(res_filtered)
print(length(rownames(res_filtered)))












