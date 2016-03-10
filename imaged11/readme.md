Mingwpy is required in order to build ImageD11 with openmp support on windows.
Mingwpy is not currently available in the default anaconda channels, so when
building the imaged11 conda package, use the following:

```
conda build -c omnia imaged11
```

(assuming your current working directory is the top-level hedm-conda-recipes)
