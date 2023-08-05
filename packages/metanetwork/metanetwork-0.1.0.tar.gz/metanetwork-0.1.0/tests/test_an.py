import pytest

from .test_fixtures import bc_dataset, iris_dataset

from metanetwork import NeuralNetwork, ArbitratedNetwork

train_X_bc, train_Y_bc, test_X_bc, test_Y_bc = bc_dataset()
train_X_iris, train_Y_iris, test_X_iris, test_Y_iris = iris_dataset()

@pytest.mark.parametrize("params", [
	({}),
	({'loss':'mse'})
])

class TestMetaNetwork:
	def test_an_binary(self, params):
		an = ArbitratedNetwork(**params)
		an.fit(train_X_bc, train_Y_bc)

	def test_an_multi(self, params):
		an = ArbitratedNetwork(**params)
		an.fit(train_X_iris, train_Y_iris)

	def test_an_predict_binary(self, params):
		an = ArbitratedNetwork(**params)
		an.fit(train_X_bc, train_Y_bc)
		an.predict(test_X_bc)

	def test_an_predict_multi(self, params):
		an = ArbitratedNetwork(**params)
		an.fit(train_X_iris, train_Y_iris)
		an.predict(test_X_iris)

def test_an_unfit():
	an = ArbitratedNetwork()
	with pytest.raises(RuntimeError):
		an.predict(test_X_bc)

def test_an_importance():
	an = ArbitratedNetwork().fit(train_X_iris, train_Y_iris)
	an.feature_importance(train_X_iris, train_Y_iris)
