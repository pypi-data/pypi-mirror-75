<p align="center">
  <img width = "500" src="./figures/stella_logo.png"/>
</p>

<p align="center">
  <a href="https://travis-ci.org/afeinstein20/stella/"><img src="https://img.shields.io/travis/afeinstein20/stella/master.svg?colorB=D35968"/></a>
  <a href="https://arxiv.org/abs/2005.07710"><img src="https://img.shields.io/badge/read-the_paper-3C1370.svg?style=flat"/></a>
  <a href="https://afeinstein20.github.io/stella/"><img src="https://img.shields.io/badge/read-the_docs-3C1370.svg?style=flat"/></a>
</p>

</p>
stella is a Python package to create and train a neural network to identify stellar flares.
Within stella, users can simulate flares as a training set, run a neural network, and feed
in their own data to the neural network model. stella returns a probability at each data point
that that data point is part of a flare or not. stella can also characterize the flares identified.
</p>


To install stella with pip:

	pip install stella

Alternatively you can install the current development version of stella:

        git clone https://github.com/afeinstein20/stella
        cd stella
        python setup.py install

If your work uses eleanor, please cite <a href="https://arxiv.org/abs/2005.07710">Feinstein et al. (submitted)</a>.

<p>
<b><u>Bug Reports, Questions, & Contributions</u></b>
</p>
<p>
stella is an open source project under the MIT license. 
The source code is available on GitHub. In case of any questions or problems, please contact us via the Git Issues. 
Pull requests are also welcome through the GitHub page.
</p>