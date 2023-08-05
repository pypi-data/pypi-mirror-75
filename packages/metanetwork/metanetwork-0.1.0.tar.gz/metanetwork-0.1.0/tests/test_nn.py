import pytest

from .test_fixtures import bc_dataset, iris_dataset

from metanetwork import NeuralNetwork

train_X_bc, train_Y_bc, test_X_bc, test_Y_bc = bc_dataset()
train_X_iris, train_Y_iris, test_X_iris, test_Y_iris = iris_dataset()

@pytest.mark.parametrize("params", [
	({}),
	({'layers':tuple()}),
	({'layers':(200,100)}),
	({'loss':'mse'}),
	({'optimizer':'sgd'}),
	({'regularizer':'l2'})
])

class TestNN:
	def test_nn_binary(self, params):
		nn = NeuralNetwork(**params)
		nn.fit(train_X_bc, train_Y_bc)

	def test_nn_multi(self, params):
		nn = NeuralNetwork(**params)
		nn.fit(train_X_iris, train_Y_iris)

	def test_nn_predict_binary(self, params):
		nn = NeuralNetwork(**params)
		nn.fit(train_X_bc, train_Y_bc)
		nn.predict(test_X_bc)

	def test_nn_predict_multi(self, params):
		nn = NeuralNetwork(**params)
		nn.fit(train_X_iris, train_Y_iris)
		nn.predict(test_X_iris)

def test_nn_unfit():
	nn = NeuralNetwork()
	with pytest.raises(RuntimeError):
		nn.predict(test_X_bc)

def test_nn_importance():
	nn = NeuralNetwork().fit(train_X_iris, train_Y_iris)
	nn.feature_importance(train_X_iris, train_Y_iris)
