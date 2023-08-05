# Changelog

## [v1.0.3.20200727](https://github.com/hackingmaterials/automatminer/tree/v1.0.3.20200727) (2020-07-28)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v1.0.3.20191111...v1.0.3.20200727)

**Implemented enhancements:**

- various doc updates [\#275](https://github.com/hackingmaterials/automatminer/issues/275)
- Keyword arg for predicted column name [\#266](https://github.com/hackingmaterials/automatminer/issues/266)

**Fixed bugs:**

- Check dfcleaner corr value works with negatively cross-correlated sampes [\#316](https://github.com/hackingmaterials/automatminer/issues/316)

**Closed issues:**

- Import fails [\#306](https://github.com/hackingmaterials/automatminer/issues/306)
- add link to arxiv paper on README / doc [\#298](https://github.com/hackingmaterials/automatminer/issues/298)
- Add Xcessiv Adaptor [\#265](https://github.com/hackingmaterials/automatminer/issues/265)

**Merged pull requests:**

- specify requirements for time being [\#299](https://github.com/hackingmaterials/automatminer/pull/299) ([ardunn](https://github.com/ardunn))
- update docs with updated matbench info [\#282](https://github.com/hackingmaterials/automatminer/pull/282) ([ardunn](https://github.com/ardunn))
- remove .needs\_oxi check in AutoFeaturizer [\#280](https://github.com/hackingmaterials/automatminer/pull/280) ([ardunn](https://github.com/ardunn))
- Add testing instructions to CONTRIBUTNG.md [\#271](https://github.com/hackingmaterials/automatminer/pull/271) ([janosh](https://github.com/janosh))
- add ability to prevent a feature cache overwrite on transform [\#269](https://github.com/hackingmaterials/automatminer/pull/269) ([ardunn](https://github.com/ardunn))
- Make name of new column with predictions appended to dataframe configurable [\#267](https://github.com/hackingmaterials/automatminer/pull/267) ([janosh](https://github.com/janosh))

## [v1.0.3.20191111](https://github.com/hackingmaterials/automatminer/tree/v1.0.3.20191111) (2019-11-12)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v1.0.2.20191110...v1.0.3.20191111)

**Implemented enhancements:**

- Look into caching via nearest neighbors  [\#194](https://github.com/hackingmaterials/automatminer/issues/194)

**Fixed bugs:**

- The .git folder is absolutely enormous.  [\#189](https://github.com/hackingmaterials/automatminer/issues/189)

**Closed issues:**

- Consider integrating with python dask [\#237](https://github.com/hackingmaterials/automatminer/issues/237)

## [v1.0.2.20191110](https://github.com/hackingmaterials/automatminer/tree/v1.0.2.20191110) (2019-11-11)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v1.0.1.20191110...v1.0.2.20191110)

**Merged pull requests:**

- update version \[skip ci\] \[ci skip\] [\#264](https://github.com/hackingmaterials/automatminer/pull/264) ([ardunn](https://github.com/ardunn))

## [v1.0.1.20191110](https://github.com/hackingmaterials/automatminer/tree/v1.0.1.20191110) (2019-11-11)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v1.0.0.20191110...v1.0.1.20191110)

## [v1.0.0.20191110](https://github.com/hackingmaterials/automatminer/tree/v1.0.0.20191110) (2019-11-10)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2019.10.14...v1.0.0.20191110)

**Implemented enhancements:**

- Enforce a code style [\#208](https://github.com/hackingmaterials/automatminer/issues/208)

**Fixed bugs:**

- Add CI for python 3.6 [\#259](https://github.com/hackingmaterials/automatminer/issues/259)

**Closed issues:**

- Fix common segfaults [\#260](https://github.com/hackingmaterials/automatminer/issues/260)
- TPOT segmentation fault [\#257](https://github.com/hackingmaterials/automatminer/issues/257)
- TypeError: can't pickle \_thread.RLock objects when saving a pipe [\#253](https://github.com/hackingmaterials/automatminer/issues/253)

**Merged pull requests:**

- add CI for 3.6 [\#263](https://github.com/hackingmaterials/automatminer/pull/263) ([ardunn](https://github.com/ardunn))
- Tpot downgrade [\#261](https://github.com/hackingmaterials/automatminer/pull/261) ([ardunn](https://github.com/ardunn))
- Add pyproject.toml to config black line length [\#258](https://github.com/hackingmaterials/automatminer/pull/258) ([janosh](https://github.com/janosh))
- Dev improvements [\#256](https://github.com/hackingmaterials/automatminer/pull/256) ([ardunn](https://github.com/ardunn))
- Logging redux [\#255](https://github.com/hackingmaterials/automatminer/pull/255) ([ardunn](https://github.com/ardunn))
- temporary workaround to avoid crashes on saving, until logging is redone [\#254](https://github.com/hackingmaterials/automatminer/pull/254) ([ardunn](https://github.com/ardunn))
- Code style enforcement [\#245](https://github.com/hackingmaterials/automatminer/pull/245) ([janosh](https://github.com/janosh))

## [v2019.10.14](https://github.com/hackingmaterials/automatminer/tree/v2019.10.14) (2019-10-15)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2019.9.11...v2019.10.14)

**Implemented enhancements:**

- More pipeline diagnostics [\#239](https://github.com/hackingmaterials/automatminer/issues/239)
- add dependabot [\#236](https://github.com/hackingmaterials/automatminer/issues/236)
- Add .from\_preset method to MatPipe [\#232](https://github.com/hackingmaterials/automatminer/issues/232)
- Change or add to digest to make it easier to read [\#221](https://github.com/hackingmaterials/automatminer/issues/221)
- Featurizer sets can be more easily rewritten as dataclasses [\#209](https://github.com/hackingmaterials/automatminer/issues/209)
- rm /tutorials and add to matminer\_examples [\#205](https://github.com/hackingmaterials/automatminer/issues/205)
- Add warning when large numbers of samples imputed/handled [\#199](https://github.com/hackingmaterials/automatminer/issues/199)

**Fixed bugs:**

- Code docs need overhaul [\#244](https://github.com/hackingmaterials/automatminer/issues/244)
- Pipeline save/load with TPOT backend doesn't attrs in intuitive way [\#241](https://github.com/hackingmaterials/automatminer/issues/241)
- MatPipe.load should refuse to load from class instance [\#234](https://github.com/hackingmaterials/automatminer/issues/234)
- Automatminer save/load needs more robust test [\#231](https://github.com/hackingmaterials/automatminer/issues/231)
- Add warning for mismatched versions of automatminer on save/load [\#230](https://github.com/hackingmaterials/automatminer/issues/230)
- Fix requirements [\#229](https://github.com/hackingmaterials/automatminer/issues/229)
- Autofeaturizer caching needs to use matminer utils, not pd.json [\#226](https://github.com/hackingmaterials/automatminer/issues/226)
- initialize\_logger has confusing arguments [\#204](https://github.com/hackingmaterials/automatminer/issues/204)

**Closed issues:**

- Reassign pipe logger [\#242](https://github.com/hackingmaterials/automatminer/issues/242)
- MatPipe save/load does not work on TPOTAdaptor pipelines [\#235](https://github.com/hackingmaterials/automatminer/issues/235)
- Add ability to MatPipe to suppress internal warnings [\#233](https://github.com/hackingmaterials/automatminer/issues/233)
- Make it easier to ignore entire columns but keep them in returned df [\#228](https://github.com/hackingmaterials/automatminer/issues/228)
- Benchdev needs a workflow for predicting properties [\#227](https://github.com/hackingmaterials/automatminer/issues/227)
- add function to matpipe to output pipeline as simple script? [\#224](https://github.com/hackingmaterials/automatminer/issues/224)
- VERSION FileNotFoundError on import [\#223](https://github.com/hackingmaterials/automatminer/issues/223)
- Add automatminer citation to all matbench datasets [\#218](https://github.com/hackingmaterials/automatminer/issues/218)
- Docs suck [\#216](https://github.com/hackingmaterials/automatminer/issues/216)
- Rewrite analytics to MatPipe [\#186](https://github.com/hackingmaterials/automatminer/issues/186)

**Merged pull requests:**

- serialize backend and test improvements [\#246](https://github.com/hackingmaterials/automatminer/pull/246) ([ardunn](https://github.com/ardunn))
- refactor setting loggers [\#243](https://github.com/hackingmaterials/automatminer/pull/243) ([janosh](https://github.com/janosh))
- Add support for pipeline digest in JSON and YAML format [\#238](https://github.com/hackingmaterials/automatminer/pull/238) ([janosh](https://github.com/janosh))

## [v2019.9.11](https://github.com/hackingmaterials/automatminer/tree/v2019.9.11) (2019-09-11)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2019.9.12...v2019.9.11)

## [v2019.9.12](https://github.com/hackingmaterials/automatminer/tree/v2019.9.12) (2019-09-11)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2019.08.07_beta...v2019.9.12)

**Closed issues:**

- benchdev needs to be updated with newest matbench v0.1 names [\#222](https://github.com/hackingmaterials/automatminer/issues/222)
- benchdev infrastructure changes [\#220](https://github.com/hackingmaterials/automatminer/issues/220)

## [v2019.08.07_beta](https://github.com/hackingmaterials/automatminer/tree/v2019.08.07_beta) (2019-08-08)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2019.08.07_betaK...v2019.08.07_beta)

## [v2019.08.07_betaK](https://github.com/hackingmaterials/automatminer/tree/v2019.08.07_betaK) (2019-08-08)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2019.05.14_beta0...v2019.08.07_betaK)

**Closed issues:**

- fix failing tests [\#215](https://github.com/hackingmaterials/automatminer/issues/215)
- remove target from predict? [\#214](https://github.com/hackingmaterials/automatminer/issues/214)
- Cannot rebuild docs? [\#213](https://github.com/hackingmaterials/automatminer/issues/213)
- Consider replacing XGBoost with Catboost [\#195](https://github.com/hackingmaterials/automatminer/issues/195)
- TPOT will, on occasion, randomly fail [\#181](https://github.com/hackingmaterials/automatminer/issues/181)
- Make an autokeras adaptor [\#147](https://github.com/hackingmaterials/automatminer/issues/147)
- Look at skater rule based models as a solution for small datasets [\#145](https://github.com/hackingmaterials/automatminer/issues/145)

## [v2019.05.14_beta0](https://github.com/hackingmaterials/automatminer/tree/v2019.05.14_beta0) (2019-05-15)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2019.03.27_beta...v2019.05.14_beta0)

**Closed issues:**

- Update xgboost version to 0.80 [\#210](https://github.com/hackingmaterials/automatminer/issues/210)
- featurization takes too much ram [\#206](https://github.com/hackingmaterials/automatminer/issues/206)
- setup.py imports automatminer  [\#202](https://github.com/hackingmaterials/automatminer/issues/202)
- Include a \(basic\) neural network separate from NNAdaptor [\#197](https://github.com/hackingmaterials/automatminer/issues/197)
- Metaselector needs a rework [\#149](https://github.com/hackingmaterials/automatminer/issues/149)

**Merged pull requests:**

- Use MultiSURF\* instead of MultiSURF [\#207](https://github.com/hackingmaterials/automatminer/pull/207) ([utf](https://github.com/utf))
- fix versioning [\#203](https://github.com/hackingmaterials/automatminer/pull/203) ([ardunn](https://github.com/ardunn))
- make DFTransformer inherit BaseEstimator [\#201](https://github.com/hackingmaterials/automatminer/pull/201) ([Qi-max](https://github.com/Qi-max))

## [v2019.03.27_beta](https://github.com/hackingmaterials/automatminer/tree/v2019.03.27_beta) (2019-03-27)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2019.03.26b0...v2019.03.27_beta)

**Merged pull requests:**

- Dev [\#200](https://github.com/hackingmaterials/automatminer/pull/200) ([ardunn](https://github.com/ardunn))

## [v2019.03.26b0](https://github.com/hackingmaterials/automatminer/tree/v2019.03.26b0) (2019-03-27)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2019.02.03_beta...v2019.03.26b0)

**Closed issues:**

- matpipe benchmark does not work with StratifiedKFold [\#191](https://github.com/hackingmaterials/automatminer/issues/191)
- Change TPOT default optimization metric to MAE? [\#190](https://github.com/hackingmaterials/automatminer/issues/190)
- PCA fails if matrix is large and n\_features \> n\_samples [\#183](https://github.com/hackingmaterials/automatminer/issues/183)
- Add "powerups" to presets [\#180](https://github.com/hackingmaterials/automatminer/issues/180)
- General problem: Featurization takes too long! [\#179](https://github.com/hackingmaterials/automatminer/issues/179)
- DataCleaner na\_method is sloppy [\#178](https://github.com/hackingmaterials/automatminer/issues/178)
- Autofeaturizer logging is annoying [\#177](https://github.com/hackingmaterials/automatminer/issues/177)
- Autofeaturizer may run redundant conversions as many as 3 times [\#176](https://github.com/hackingmaterials/automatminer/issues/176)
- Add circleci test for 3.7 [\#175](https://github.com/hackingmaterials/automatminer/issues/175)
- Logger should append to existing logs, not overwrite it [\#174](https://github.com/hackingmaterials/automatminer/issues/174)
- Analytics tests should run whether or not they are on circleci [\#169](https://github.com/hackingmaterials/automatminer/issues/169)
- Real docs + more thorough example [\#167](https://github.com/hackingmaterials/automatminer/issues/167)
- Add option to control tree and correlation-based FeatureReducer  params [\#162](https://github.com/hackingmaterials/automatminer/issues/162)
- Use MEGNet/CGCNN as backend? [\#156](https://github.com/hackingmaterials/automatminer/issues/156)
- Need more featurizers implemented in matminer/automatminer [\#143](https://github.com/hackingmaterials/automatminer/issues/143)
- Outlier detection as a preprocessing step [\#135](https://github.com/hackingmaterials/automatminer/issues/135)
- Look into FunctionFeaturizer [\#134](https://github.com/hackingmaterials/automatminer/issues/134)
- Analysis class needs to be beefed up with something actually useful [\#105](https://github.com/hackingmaterials/automatminer/issues/105)
- Analysis should produce summary and visualization as file [\#57](https://github.com/hackingmaterials/automatminer/issues/57)

**Merged pull requests:**

- Documentation is completed [\#198](https://github.com/hackingmaterials/automatminer/pull/198) ([samysspace](https://github.com/samysspace))
- Edits1 [\#196](https://github.com/hackingmaterials/automatminer/pull/196) ([ardunn](https://github.com/ardunn))
- changing base classes [\#187](https://github.com/hackingmaterials/automatminer/pull/187) ([ardunn](https://github.com/ardunn))

## [v2019.02.03_beta](https://github.com/hackingmaterials/automatminer/tree/v2019.02.03_beta) (2019-02-03)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2019.02.02_beta...v2019.02.03_beta)

## [v2019.02.02_beta](https://github.com/hackingmaterials/automatminer/tree/v2019.02.02_beta) (2019-02-02)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2019.01.26_beta...v2019.02.02_beta)

**Closed issues:**

- Nose ---\> unittest  [\#171](https://github.com/hackingmaterials/automatminer/issues/171)
- Fix benchmarking [\#170](https://github.com/hackingmaterials/automatminer/issues/170)
- Should add to PyPi [\#168](https://github.com/hackingmaterials/automatminer/issues/168)
- An adapter to run a single model [\#165](https://github.com/hackingmaterials/automatminer/issues/165)
- Add option to remove specific features [\#159](https://github.com/hackingmaterials/automatminer/issues/159)
- Analytics module needs tests [\#133](https://github.com/hackingmaterials/automatminer/issues/133)

**Merged pull requests:**

- Update codacy and circleCI configs [\#173](https://github.com/hackingmaterials/automatminer/pull/173) ([utf](https://github.com/utf))
- Add optional to manually keep/remove features [\#172](https://github.com/hackingmaterials/automatminer/pull/172) ([utf](https://github.com/utf))

## [v2019.01.26_beta](https://github.com/hackingmaterials/automatminer/tree/v2019.01.26_beta) (2019-01-26)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2019.01.25_beta...v2019.01.26_beta)

**Closed issues:**

- MatPipe code needs revamp [\#166](https://github.com/hackingmaterials/automatminer/issues/166)
- Implement nested CV for pipeline benchmarking [\#163](https://github.com/hackingmaterials/automatminer/issues/163)
- CircleCI + package reqs  needs update [\#150](https://github.com/hackingmaterials/automatminer/issues/150)

## [v2019.01.25_beta](https://github.com/hackingmaterials/automatminer/tree/v2019.01.25_beta) (2019-01-26)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/2018.12.11_beta...v2019.01.25_beta)

**Closed issues:**

- List-like test\_spec behavior broken in benchmark function [\#161](https://github.com/hackingmaterials/automatminer/issues/161)
- Add random\_state option to benchmark function [\#160](https://github.com/hackingmaterials/automatminer/issues/160)
- Autofeaturizer needs ability to use custom column names [\#148](https://github.com/hackingmaterials/automatminer/issues/148)
- Add jarvis to AllFeaturizers [\#144](https://github.com/hackingmaterials/automatminer/issues/144)
- Empty logger made anytime MatPipe imported [\#141](https://github.com/hackingmaterials/automatminer/issues/141)
- removing correlated features doesn't work for classification targets [\#140](https://github.com/hackingmaterials/automatminer/issues/140)
- Oxidation states guessed twice [\#138](https://github.com/hackingmaterials/automatminer/issues/138)
- Look into using NestedCV for automl, and whether it would be a good idea or not [\#130](https://github.com/hackingmaterials/automatminer/issues/130)
- Add a very simple example [\#108](https://github.com/hackingmaterials/automatminer/issues/108)
- Add another study comparison with matbench [\#65](https://github.com/hackingmaterials/automatminer/issues/65)
- Add a profiler to DataframeTransformer [\#56](https://github.com/hackingmaterials/automatminer/issues/56)

**Merged pull requests:**

- Added Examples Folder and MSE Example [\#158](https://github.com/hackingmaterials/automatminer/pull/158) ([ADA110](https://github.com/ADA110))
- Analytics Module Tests [\#157](https://github.com/hackingmaterials/automatminer/pull/157) ([ADA110](https://github.com/ADA110))
- \(WIP\) Custom Column Names [\#152](https://github.com/hackingmaterials/automatminer/pull/152) ([ADA110](https://github.com/ADA110))
- Better handling of adding oxidation states to large structures. [\#142](https://github.com/hackingmaterials/automatminer/pull/142) ([utf](https://github.com/utf))

## [2018.12.11_beta](https://github.com/hackingmaterials/automatminer/tree/2018.12.11_beta) (2018-12-12)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2018.11.16-beta...2018.12.11_beta)

**Closed issues:**

-  No module named 'automatminer.featurize' [\#146](https://github.com/hackingmaterials/automatminer/issues/146)
- metaselection needs error handling, or screening beforehand [\#139](https://github.com/hackingmaterials/automatminer/issues/139)
- Add logging warning level option to Matpipe object. [\#136](https://github.com/hackingmaterials/automatminer/issues/136)
- Add ability to ensemble top models in tpot [\#111](https://github.com/hackingmaterials/automatminer/issues/111)
- Make dataset test set [\#107](https://github.com/hackingmaterials/automatminer/issues/107)
- Consider adaptor classes for other backends [\#100](https://github.com/hackingmaterials/automatminer/issues/100)
- Using skater for analysis [\#95](https://github.com/hackingmaterials/automatminer/issues/95)
- Tpot defaults need investigation and modification [\#79](https://github.com/hackingmaterials/automatminer/issues/79)
- Add more featurizers to AllFeaturizers [\#60](https://github.com/hackingmaterials/automatminer/issues/60)

**Merged pull requests:**

- Add logging level option to pipeline object [\#137](https://github.com/hackingmaterials/automatminer/pull/137) ([utf](https://github.com/utf))
- Basic Analytics Tools [\#132](https://github.com/hackingmaterials/automatminer/pull/132) ([Doppe1g4nger](https://github.com/Doppe1g4nger))
- dev\_scripts draft for evaluation + various fixes [\#131](https://github.com/hackingmaterials/automatminer/pull/131) ([ardunn](https://github.com/ardunn))

## [v2018.11.16-beta](https://github.com/hackingmaterials/automatminer/tree/v2018.11.16-beta) (2018-11-17)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2018.11.2-beta...v2018.11.16-beta)

## [v2018.11.2-beta](https://github.com/hackingmaterials/automatminer/tree/v2018.11.2-beta) (2018-11-17)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/v2018.11.2-alpha...v2018.11.2-beta)

**Closed issues:**

- MatPipe cannot be serialized [\#124](https://github.com/hackingmaterials/automatminer/issues/124)
- MatPipe needs tests [\#118](https://github.com/hackingmaterials/automatminer/issues/118)
- DataCleaner needs scaling [\#115](https://github.com/hackingmaterials/automatminer/issues/115)
- Logger problems [\#114](https://github.com/hackingmaterials/automatminer/issues/114)
- Remove temp fix of CompositionToOxidComposition with next matminer [\#113](https://github.com/hackingmaterials/automatminer/issues/113)
- Tpot tests need to be redone [\#109](https://github.com/hackingmaterials/automatminer/issues/109)
- Top level classes should be able to serialize all pipeline info to json [\#102](https://github.com/hackingmaterials/automatminer/issues/102)
- Top level class methods need work [\#97](https://github.com/hackingmaterials/automatminer/issues/97)
- Tests need coverage assessment [\#83](https://github.com/hackingmaterials/automatminer/issues/83)
- Dataset storage needs improvement [\#80](https://github.com/hackingmaterials/automatminer/issues/80)

**Merged pull requests:**

- update benchmark on matpipe and update test [\#129](https://github.com/hackingmaterials/automatminer/pull/129) ([ardunn](https://github.com/ardunn))
- Add matpipe tests, digest, and ability to save and load pipes [\#127](https://github.com/hackingmaterials/automatminer/pull/127) ([ardunn](https://github.com/ardunn))
- MatPipe improvements + tpot tests [\#126](https://github.com/hackingmaterials/automatminer/pull/126) ([ardunn](https://github.com/ardunn))
- Refactor mslearn to use matminer for its dataset needs [\#125](https://github.com/hackingmaterials/automatminer/pull/125) ([Doppe1g4nger](https://github.com/Doppe1g4nger))
- remove conversion override and fix log typos [\#123](https://github.com/hackingmaterials/automatminer/pull/123) ([ardunn](https://github.com/ardunn))
- quick update verbosity of adaptor [\#122](https://github.com/hackingmaterials/automatminer/pull/122) ([ardunn](https://github.com/ardunn))
- big ol refactor + matpipe updates [\#121](https://github.com/hackingmaterials/automatminer/pull/121) ([ardunn](https://github.com/ardunn))
- make metaselection part of AutoFeaturizer [\#120](https://github.com/hackingmaterials/automatminer/pull/120) ([Qi-max](https://github.com/Qi-max))
- Fix pipeline logger [\#119](https://github.com/hackingmaterials/automatminer/pull/119) ([utf](https://github.com/utf))

## [v2018.11.2-alpha](https://github.com/hackingmaterials/automatminer/tree/v2018.11.2-alpha) (2018-11-02)

[Full Changelog](https://github.com/hackingmaterials/automatminer/compare/cc9702425531022dc76caf6bdc574be34b5c5ae8...v2018.11.2-alpha)

**Closed issues:**

- Logger needed [\#103](https://github.com/hackingmaterials/automatminer/issues/103)
- Heuristic based featurizer selection [\#99](https://github.com/hackingmaterials/automatminer/issues/99)
- ++robustness and usefulness of featurizer sets [\#98](https://github.com/hackingmaterials/automatminer/issues/98)
- Convert preprocessing modele into 2 separate operations [\#96](https://github.com/hackingmaterials/automatminer/issues/96)
- Adding/converting .fit/.transform/.predict methods [\#92](https://github.com/hackingmaterials/automatminer/issues/92)
- Further package structure suggestions [\#88](https://github.com/hackingmaterials/automatminer/issues/88)
- Rename AutoML segment of pipeline to better reflect package use [\#87](https://github.com/hackingmaterials/automatminer/issues/87)
- Plan - WIP [\#85](https://github.com/hackingmaterials/automatminer/issues/85)
- TestAllFeaturizers will break whenever a new featurizer is added [\#82](https://github.com/hackingmaterials/automatminer/issues/82)
- test\_tpot hard to maintain with tpot version update [\#73](https://github.com/hackingmaterials/automatminer/issues/73)
- Dimensionality reduction [\#61](https://github.com/hackingmaterials/automatminer/issues/61)
- matminer issue: MaximumPackingEfficiency error [\#59](https://github.com/hackingmaterials/automatminer/issues/59)
- set mpid as index if available in load\_\* functions [\#58](https://github.com/hackingmaterials/automatminer/issues/58)
- Castelli is missing structure or the doc is incorrect [\#54](https://github.com/hackingmaterials/automatminer/issues/54)
- Testing takes unacceptably long times [\#49](https://github.com/hackingmaterials/automatminer/issues/49)
- zhou gaps formula can't be converted to composition [\#38](https://github.com/hackingmaterials/automatminer/issues/38)
- Model Selection Methodology [\#33](https://github.com/hackingmaterials/automatminer/issues/33)
- normalize preprocess for the future use of pipeline [\#20](https://github.com/hackingmaterials/automatminer/issues/20)
- find a way to obtain feature\_cols list and target\_col easily [\#19](https://github.com/hackingmaterials/automatminer/issues/19)
- load\_\* functions should ensure all numeric columns [\#16](https://github.com/hackingmaterials/automatminer/issues/16)
- load\_mp should return other quantities [\#15](https://github.com/hackingmaterials/automatminer/issues/15)
- all formula columns in load\_\* funcs should return Composition objects [\#14](https://github.com/hackingmaterials/automatminer/issues/14)
- What is MatbenchError? [\#11](https://github.com/hackingmaterials/automatminer/issues/11)

**Merged pull requests:**

- Adding top level class + bugfixes [\#117](https://github.com/hackingmaterials/automatminer/pull/117) ([ardunn](https://github.com/ardunn))
- change logging default and show example [\#116](https://github.com/hackingmaterials/automatminer/pull/116) ([ardunn](https://github.com/ardunn))
- a base to start from [\#112](https://github.com/hackingmaterials/automatminer/pull/112) ([ardunn](https://github.com/ardunn))
- Matbench wide logger [\#110](https://github.com/hackingmaterials/automatminer/pull/110) ([utf](https://github.com/utf))
- Improve metalearning for automatically filter featurizers [\#106](https://github.com/hackingmaterials/automatminer/pull/106) ([Qi-max](https://github.com/Qi-max))
- add cv docs + citations and implementors methods [\#104](https://github.com/hackingmaterials/automatminer/pull/104) ([albalu](https://github.com/albalu))
- add TreeBasedFeatureReduction + tests [\#101](https://github.com/hackingmaterials/automatminer/pull/101) ([albalu](https://github.com/albalu))
- Adding top level class skeleton and jarvis dataset [\#94](https://github.com/hackingmaterials/automatminer/pull/94) ([ardunn](https://github.com/ardunn))
- Update dataset loading utilities to use new function [\#93](https://github.com/hackingmaterials/automatminer/pull/93) ([Doppe1g4nger](https://github.com/Doppe1g4nger))
- organize preprocess just a bit [\#91](https://github.com/hackingmaterials/automatminer/pull/91) ([albalu](https://github.com/albalu))
- Improved testing of AllFeaturizers class [\#90](https://github.com/hackingmaterials/automatminer/pull/90) ([utf](https://github.com/utf))
- Update conversions to use conversion featurizers [\#89](https://github.com/hackingmaterials/automatminer/pull/89) ([utf](https://github.com/utf))
- make subpackages and their importing consistent [\#86](https://github.com/hackingmaterials/automatminer/pull/86) ([albalu](https://github.com/albalu))
- consistent naming [\#84](https://github.com/hackingmaterials/automatminer/pull/84) ([albalu](https://github.com/albalu))
- Organize file structure, add a dataset + more [\#81](https://github.com/hackingmaterials/automatminer/pull/81) ([ardunn](https://github.com/ardunn))
- Code cleanup on tpot\_utils [\#78](https://github.com/hackingmaterials/automatminer/pull/78) ([Doppe1g4nger](https://github.com/Doppe1g4nger))
- Cleanup is\_greater\_better function  [\#76](https://github.com/hackingmaterials/automatminer/pull/76) ([Doppe1g4nger](https://github.com/Doppe1g4nger))
- fix logger issue duplicated in notebooks [\#75](https://github.com/hackingmaterials/automatminer/pull/75) ([albalu](https://github.com/albalu))
- Add classifier/regressor config\_dicts for customizing pipeline operators [\#74](https://github.com/hackingmaterials/automatminer/pull/74) ([Qi-max](https://github.com/Qi-max))
- Split + improve existing glass datasets and add a new dataset [\#72](https://github.com/hackingmaterials/automatminer/pull/72) ([Qi-max](https://github.com/Qi-max))
- Change default for max\_na\_frac, add notebook [\#71](https://github.com/hackingmaterials/automatminer/pull/71) ([ardunn](https://github.com/ardunn))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
