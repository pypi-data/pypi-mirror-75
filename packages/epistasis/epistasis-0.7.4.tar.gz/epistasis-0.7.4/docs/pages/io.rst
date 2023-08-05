Saving an epistasis model
=========================

All epistasis models/simulators store epistatic coefficients in Pandas_ Series/DataFrames, so the coefficients can be written to various file formats. This page lists a few.

.. _Pandas: http://pandas.pydata.org/

Pickle
------

The recommended way to save an epistasis model to be used again is by **pickling** the model(See Python's ``pickle`` library).

.. code-block:: python

  # Import pickle module
  import pickle
  from epistasis.models import EpistasisLinearRegression

  # Simple model object
  model = EpistasisLinearRegression(model=1)

  # Save to disk to open later.
  with open('model.pickle', 'wb') as f:
      pickle.dump(f, model)

To load the saved model,

.. code-block:: python

  # Import pickle module
  import pickle

  # Read from file.
  with open('model.pickle', 'rb') as f:
      model = pickle.load(f)

.. warning::

  Pickled models will only work with the same version of the ``epistasis``
  package that created it. If you save a model and upgrade the library, you likely
  won't be able to use the model anymore.


Excel Spreadsheet
-----------------

Epistatic coefficients can be written to an excel file using the ``to_excel`` method

.. code-block:: python

  model.to_excel('data.xlsx')

.. raw:: html


  <table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sites</th>
      <th>values</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>[0]</td>
      <td>0.501191</td>
    </tr>
    <tr>
      <th>1</th>
      <td>[1]</td>
      <td>-0.600019</td>
    </tr>
    <tr>
      <th>2</th>
      <td>[2]</td>
      <td>0.064983</td>
    </tr>
    <tr>
      <th>3</th>
      <td>[3]</td>
      <td>0.609166</td>
    </tr>
    <tr>
      <th>4</th>
      <td>[4]</td>
      <td>0.242095</td>
    </tr>
    <tr>
      <th>5</th>
      <td>[1, 2]</td>
      <td>0.286914</td>
    </tr>
    <tr>
      <th>6</th>
      <td>[1, 3]</td>
      <td>-0.264455</td>
    </tr>
    <tr>
      <th>7</th>
      <td>[1, 4]</td>
      <td>-0.464212</td>
    </tr>
    <tr>
      <th>8</th>
      <td>[2, 3]</td>
      <td>0.638260</td>
    </tr>
    <tr>
      <th>9</th>
      <td>[2, 4]</td>
      <td>0.235989</td>
    </tr>
    <tr>
      <th>10</th>
      <td>[3, 4]</td>
      <td>0.717954</td>
    </tr>
    <tr>
      <th>11</th>
      <td>[1, 2, 3]</td>
      <td>-0.473122</td>
    </tr>
    <tr>
      <th>12</th>
      <td>[1, 2, 4]</td>
      <td>-0.041919</td>
    </tr>
    <tr>
      <th>13</th>
      <td>[1, 3, 4]</td>
      <td>-0.309124</td>
    </tr>
    <tr>
      <th>14</th>
      <td>[2, 3, 4]</td>
      <td>0.606674</td>
    </tr>
    <tr>
      <th>15</th>
      <td>[1, 2, 3, 4]</td>
      <td>-0.268982</td>
    </tr>
  </tbody>
  </table>


CSV File
--------

Epistatic coefficients can be written to a csv file using the ``to_csv`` method

.. code-block:: python

  model.epistasis.to_csv('epistasis.csv')


.. code-block:: none

  ,sites,values
  0,[0],0.5011910655025966
  1,[1],-0.6000186681513706
  2,[2],0.06498276930060931
  3,[3],0.6091656756721153
  4,[4],0.24209508436556937
  5,"[1, 2]",0.2869142038187855
  6,"[1, 3]",-0.26445514455225094
  7,"[1, 4]",-0.4642116520437949
  8,"[2, 3]",0.638260262428922
  9,"[2, 4]",0.23598864236123118
  10,"[3, 4]",0.7179538630349485
  11,"[1, 2, 3]",-0.47312160287366267
  12,"[1, 2, 4]",-0.04191888437610514
  13,"[1, 3, 4]",-0.30912353449573415
  14,"[2, 3, 4]",0.6066739725656609
  15,"[1, 2, 3, 4]",-0.2689818206753505
