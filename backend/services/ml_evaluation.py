import torch
import torch.nn as nn
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import logging

logger = logging.getLogger(__name__)

class ModelEvaluator:
    def __init__(self, model: nn.Module, device: str = 'cuda'):
        self.model = model.to(device)
        self.device = device
        self.model.eval()
    
    def evaluate(self, dataloader):
        all_preds = []
        all_targets = []
        with torch.no_grad():
            for inputs, targets in dataloader:
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)
                outputs = self.model(inputs)
                preds = torch.argmax(outputs, dim=1)
                all_preds.extend(preds.cpu().numpy())
                all_targets.extend(targets.cpu().numpy())
        all_preds = np.array(all_preds)
        all_targets = np.array(all_targets)
        accuracy = accuracy_score(all_targets, all_preds)
        precision = precision_score(all_targets, all_preds, average='weighted', zero_division=0)
        recall = recall_score(all_targets, all_preds, average='weighted', zero_division=0)
        f1 = f1_score(all_targets, all_preds, average='weighted', zero_division=0)
        logger.info(f"Eval: Acc={accuracy:.4f}, F1={f1:.4f}")
        return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1_score': f1}
