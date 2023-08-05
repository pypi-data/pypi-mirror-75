import pytest
import numpy as np
from sklearn.datasets import load_breast_cancer, load_iris

def bc_dataset():
	dataset = load_breast_cancer()
	data = dataset['data']
	data = (data - np.mean(data, axis=0)) / np.std(data, axis=0)
	min, max = data.min(axis=0), data.max(axis=0)
	data = (data - min) / (max - min)
	target = dataset['target']
	partition = int(0.8 * len(data))
	train_X_bc = data[:partition]
	train_Y_bc = target[:partition]
	test_X_bc = data[partition:]
	test_Y_bc = target[partition:]
	return train_X_bc, train_Y_bc, test_X_bc, test_Y_bc

def iris_dataset():
	dataset = load_iris()
	data = dataset['data']
	data = (data - np.mean(data, axis=0)) / np.std(data, axis=0)
	min, max = data.min(axis=0), data.max(axis=0)
	data = (data - min) / (max - min)
	target = dataset['target']
	partition = int(0.8 * len(data))
	train_X_iris = data[:partition]
	train_Y_iris = target[:partition]
	test_X_iris = data[partition:]
	test_Y_iris = target[partition:]
	return train_X_iris, train_Y_iris, test_X_iris, test_Y_iris
