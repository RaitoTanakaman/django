import tez
import pandas as pd
import torch
import torch.nn as nn
from sklearn import model_selection
from sklearn import metrics, preprocessing
import numpy as np


class CampsitesDataset:

    def __init__(self, users, campsites, scores):
        self.users = users
        self.campsites = campsites
        self.scores = scores

    def __len__(self):
        return len(self.users)

    def __getitem__(self, item):
        user = self.users[item]
        campsite = self.campsites[item]
        score = self.scores[item]

        return {
            'user': torch.tensor(user, dtype=torch.long),
            'campsite': torch.tensor(campsite, dtype=torch.long),
            'score': torch.tensor(score, dtype=torch.float),
        }


class RecSysModel(tez.Model):

    def __init__(self, num_users, num_campsites):
        super().__init__()
        self.user_embed = nn.Embedding(num_users, 32)
        self.campsite_embed = nn.Embedding(num_campsites, 32)
        self.out = nn.Linear(64, 1)
        self.step_scheduler_after = 'epoch'

    def fetch_optimizer(self):
        opt = torch.optim.Adam(self.parameters(), lr=le-3)

        return opt

    def fetch_scheduler(self):
        sch = torch.optim.lr_scheduler.StemLR(
            self.optimizer, step_size=3, gamma=0.7)

        return sch

    def monitor_metrics(self, output, score):
        output = output.detach().cpu().numpy()
        score = score.detach().cpu().numpy()

        return {
            'rmse': np.sqrt(metrics.mean_squared_error(score, output))
        }

    def forward(self, users, campsites, scores=None):
        user_embeds = self.user_embed(users)
        campsite_embeds = self.campsite_embed(campsites)
        output = torch.cat([user_embeds, campsite_embeds], dim=1)
        output = self.out(output)
        loss = nn.MSELoss()(output, scores.view(-1, 1))
        calc_metrics = self.monitor_metorics(output, scores.view(-1, 1))

        return output, loss, calc_metrics


def train():
    df = pd.read_pickle('campsites_ratings.pickle')
    lbl_user = preprocessing.LabelEncoder()
    lbl_campsite = preprocessing.LabelEncoder()
    df[0] = lbl_user.fit_transform(df[0].values)
    df[1] = lbl_campsite.fit_transform(df[1].values)
    df_train, df_valid = model_selection.train_test_split(
        df, test_size=0.1, random_state=42, stratify=df[2].values)
    train_dataset = CampsitesDataset(
        users=df_train[0].values, campsites=df_train[1].values, scores=df_train[2].values)
    valid_dataset = CampsitesDataset(
        users=df_train[0].values, campsites=df_train[1].values, scores=df_train[2].values)
    model = RecSysModel(num_users=len(lbl_user.classes_),
                        num_campsites=len(lbl_campsite.classes_))
    model.fit(train_dataset, valid_dataset,
              train_bs=1024, valid_bs=1024, fp16=True)


if __name__ == '__main__':
    train()
