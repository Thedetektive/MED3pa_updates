import os
import json
import matplotlib.pyplot as plt
INTERNAL_FILE_PATH = r"C:\Users\thanh\Documents\Work\MEDomics\med3pa\study_3pa\experiments\results\in_hospital_mortality\Internal\MED3paResults_20260525113551.MED3paResults"

with open(INTERNAL_FILE_PATH,'r') as f:
    data = json.load(f)

print(data["loadedFiles"]["test"]["profiles"]['0']['100'][1]['node information'])
# x_auc = range(1,101)
# y_auc = []
# for i in range(1,101):
#     y_auc.append(data["loadedFiles"]["test"]["metrics_dr"][str(i)]['metrics']['Auc'])
# plt.plot(x_auc,y_auc,label="AUC Score")
# x_f1 = range(1,101)
# y_f1 = []
# for i in range(1,101):
#     y_f1.append(data["loadedFiles"]["test"]["metrics_dr"][str(i)]['metrics']['F1Score'])
# plt.plot(x_f1,y_f1,label="F1 Score")
# plt.legend()
# plt.show()