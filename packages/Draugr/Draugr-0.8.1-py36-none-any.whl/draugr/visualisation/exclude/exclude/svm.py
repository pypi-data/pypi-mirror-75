#!/usr/bin/env python
import itertools
import pickle

from matplotlib import pyplot
import numpy
import pysnooper
from sklearn import cross_validation, metrics, svm
from sklearn.preprocessing import LabelEncoder, StandardScaler


@pysnooper.snoop()
def plot_confusion_matrix(cm, classes, normalize=False,
                          title='Confusion matrix', cmap=pyplot.cm.Blues):
  """This function prints and plots the confusion matrix. Normalization can
  be applied by setting `normalize=True`.
  """

  pyplot.imshow(cm, interpolation='nearest', cmap=cmap)
  pyplot.title(title)
  pyplot.colorbar()
  tick_marks = numpy.arange(len(classes))
  pyplot.xticks(tick_marks, classes, rotation=45)
  pyplot.yticks(tick_marks, classes)

  if normalize:
    cm = cm.astype('float') / cm.sum(axis=1)[:, numpy.newaxis]

  thresh = cm.max() / 2.
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    pyplot.text(j, i, '{0:.2f}'.format(cm[i, j]),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black")

  pyplot.tight_layout()
  pyplot.ylabel('True label')
  pyplot.xlabel('Predicted label')


# Load training data from disk
training_set = pickle.load(open('training_set_pr2.sav', 'rb'))

# Format the features and labels for use with scikit learn
feature_list = []
label_list = []

for item in training_set:
  if numpy.isnan(item[0]).sum() < 1:
    feature_list.append(item[0])
    label_list.append(item[1])

print('Features in Training Set: {}'.format(len(training_set)))
print('Invalid Features in Training set: {}'.format(len(training_set) - len(feature_list)))

X = numpy.array(feature_list)
# Fit a per-column scaler
X_scaler = StandardScaler().fit(X)
# Apply the scaler to X
X_train = X_scaler.transform(X)
y_train = numpy.array(label_list)

# Convert label strings to numerical encoding
encoder = LabelEncoder()
y_train = encoder.fit_transform(y_train)

# Create classifier
clf = svm.SVC(kernel='linear', C=0.1)

# Set up 5-fold cross-validation
cval = cross_validation.KFold(len(X_train),
                              n_folds=50,
                              shuffle=True,
                              random_state=30)
# cval = cross_validation.LeaveOneOut(len(X_train))

# Perform cross-validation
scores = cross_validation.cross_val_score(cv=cval,
                                          estimator=clf,
                                          X=X_train,
                                          y=y_train,
                                          scoring='accuracy'
                                          )
print('Scores: %s' % str(scores))
print('Accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), 2 * scores.std()))

# Gather predictions
predictions = cross_validation.cross_val_predict(cv=cval,
                                                 estimator=clf,
                                                 X=X_train,
                                                 y=y_train
                                                 )

accuracy_score = metrics.accuracy_score(y_train, predictions)
print('Accuracy score: %s' % str(accuracy_score))

confusion_matrix = metrics.confusion_matrix(y_train, predictions)

class_names = encoder.classes_.tolist()

# Train the classifier
clf.fit(X=X_train, y=y_train)

model = {'classifier':clf, 'classes':encoder.classes_, 'scaler':X_scaler}

# Save classifier to disk
pickle.dump(model, open('model.sav', 'wb'))

# Plot non-normalized confusion matrix
pyplot.figure()
plot_confusion_matrix(confusion_matrix, classes=encoder.classes_,
                      title='Confusion matrix, without normalization')

# Plot normalized confusion matrix
pyplot.figure()
plot_confusion_matrix(confusion_matrix, classes=encoder.classes_, normalize=True,
                      title='Normalized confusion matrix')

pyplot.show()
