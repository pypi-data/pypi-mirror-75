keras_mixed_sequence
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy|
|code_climate_maintainability| |pip| |downloads|

Lazily loading mixed sequences using Keras Sequence,
focused on multi-task models.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install keras_mixed_sequence

Tests Coverage
----------------------------------------------
Since some software handling coverages sometimes get
slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Usage examples
----------------------------------------------

Example for traditional single-task models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
First of all let's create a simple single-task model:

.. code:: python

    from tensorflow.keras.layers import Dense
    from tensorflow.keras.models import Sequential

    model = Sequential([
        Dense(1, activation="relu")
    ])
    model.compile(
        optimizer="nadam",
        loss="relu"
    )

Then we proceed to load or otherwise create the training data.
Here there will be listed, in the future, some custom
Sequence objects that have been created for the purpose
of being used alongside this library.

.. code:: python

    X = either_a_numpy_array_or_sequence_for_input
    y = either_a_numpy_array_or_sequence_for_output

Now we combine the training data using the MixedSequence
object.

.. code:: python

    from keras_mixed_sequence import MixedSequence

    sequence = MixedSequence(
        X, y,
        batch_size=batch_size
    )

Finally, we can train the model:

.. code:: python

    from multiprocessing import cpu_count

    model.fit_generator(
        sequence,
        steps_per_epoch=sequence.steps_per_epoch,
        epochs=2,
        verbose=0,
        use_multiprocessing=True,
        workers=cpu_count(),
        shuffle=True
    )


Example for multi-task models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
First of all let's create a simple multi-taks model:

.. code:: python

    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Dense, Input

    inputs = Input(shape=(10,))

    output1 = Dense(
        units=10,
        activation="relu",
        name="output1"
    )(inputs)
    output2 = Dense(
        units=10,
        activation="relu",
        name="output2"
    )(inputs)

    model = Model(
        inputs=inputs,
        outputs=[output1, output2],
        name="my_model"
    )

    model.compile(
        optimizer="nadam",
        loss="MSE"
    )

Then we proceed to load or otherwise create the training data.
Here there will be listed, in the future, some custom
Sequence objects that have been created for the purpose
of being used alongside this library.

.. code:: python

    X = either_a_numpy_array_or_sequence_for_input
    y1 = either_a_numpy_array_or_sequence_for_output1
    y2 = either_a_numpy_array_or_sequence_for_output2

Now we combine the training data using the MixedSequence
object.

.. code:: python

    from keras_mixed_sequence import MixedSequence

    sequence = MixedSequence(
        x=X,
        y={
            "output1": y1,
            "output2": y2
        },
        batch_size=batch_size
    )

Finally, we can train the model:

.. code:: python

    from multiprocessing import cpu_count

    model.fit_generator(
        sequence,
        steps_per_epoch=sequence.steps_per_epoch,
        epochs=2,
        verbose=0,
        use_multiprocessing=True,
        workers=cpu_count(),
        shuffle=True
    )

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/keras_mixed_sequence.png
   :target: https://travis-ci.org/LucaCappelletti94/keras_mixed_sequence
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_keras_mixed_sequence&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_keras_mixed_sequence
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_keras_mixed_sequence&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_keras_mixed_sequence
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_keras_mixed_sequence&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_keras_mixed_sequence
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/keras_mixed_sequence/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/keras_mixed_sequence?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/keras-mixed-sequence.svg
    :target: https://badge.fury.io/py/keras-mixed-sequence
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/keras-mixed-sequence
    :target: https://pepy.tech/badge/keras-mixed-sequence
    :alt: Pypi total project downloads

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/249884df3ba34204850ac2448a9b176d
    :target: https://www.codacy.com/manual/LucaCappelletti94/keras_mixed_sequence?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/keras_mixed_sequence&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/b5ec3fe894a0f561f7e1/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/keras_mixed_sequence/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/b5ec3fe894a0f561f7e1/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/keras_mixed_sequence/test_coverage
    :alt: Code Climate Coverate
