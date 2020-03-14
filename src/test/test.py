import glob
import os
import pickle

from tqdm import tqdm

mc_path = '../../Dataset/models/mc.dat'
pe = '../../Dataset/pe'
train = '../../Dataset/train'
label_file = '../../Dataset/trainLabels.csv'
label_file_new = '../../Dataset/trainLabels_new.csv'

mc_map = pickle.load(open(mc_path, 'rb'))

content = []
content_new = []
with open(label_file, 'r') as csv:
    content = csv.readlines()
    content_new = content

del_pe_count = 0
del_bytes_count = 0
del_label_count = 0
for filename, tuple in mc_map.items():
    # 删除pe目录样本
    fold_list = os.listdir(pe)
    for i, fold in enumerate(fold_list):
        files = os.listdir(os.path.join(pe, fold))
        for f in files:
            if f == filename:
                os.remove(os.path.join(os.path.join(pe, fold), f))
                del_pe_count += 1

    # 删除.bytes
    ff = os.path.join(train, filename + '.bytes')
    if os.path.exists(ff):
        os.remove(ff)
        del_bytes_count += 1

    # 重新构造trainLabel.csv
    for cc in content:
        if filename + '.bytes' in cc:
            content_new.remove(cc)
            del_label_count += 1

print("原有{}个pe样本，删除{}个".format(len(content) - 1, del_pe_count))
print("删除{}个bytes文件".format(del_bytes_count))
print("原有{}个label，删除{}个label，content_new剩余{}个"
      .format(len(content) - 1, del_label_count, len(content_new) - 1))

re_del_bytes_count = 0
# 再次清理bytes
bytes = os.listdir(train)
tqdm_bytes = tqdm(bytes)
for bb in tqdm_bytes:
    tqdm_bytes.set_description(bb)
    del_flag = True
    for ll in content_new:
        if bb.replace('.bytes', '') in ll:
            del_flag = False
            break
    if del_flag:
        os.remove(os.path.join(train, bb))
        re_del_bytes_count += 1

print("重新清理{}个bytes文件，剩余{}个".format(re_del_bytes_count, len(glob.glob(os.path.join(train, "*.bytes")))))

with open(label_file, 'w') as csv:
    csv.writelines(content_new)
