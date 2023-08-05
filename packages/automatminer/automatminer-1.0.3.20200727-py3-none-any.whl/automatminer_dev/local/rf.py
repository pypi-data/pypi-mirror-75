from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import pandas as pd
from automatminer import (
    AutoFeaturizer,
    DataCleaner,
    FeatureReducer,
    TPOTAdaptor,
    MatPipe,
)
from sklearn.model_selection import train_test_split
from automatminer.automl.adaptors import SinglePipelineAdaptor
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold

path = "/Users/ardunn/alex/lbl/projects/common_env/dev_codes/automatminer/automatminer_dev/testing/datasets/glass.pickle.gz"
df = pd.read_pickle(path)

target = "gfa"

kf = KFold(n_splits=5, shuffle=True, random_state=1001)
splits = [s for s in kf.split(df.index)]
train, test = splits[0]


# train, test = train_test_split(df.index, test_size=0.2, shuffle=True, random_state=1001)


# print(type(train))
# print(type(test))


for t in train:
    if t in test:
        print(f"WOAH: {t}")

# print(train)
# print(type(train))
# print(train.shape)
# print("------")
# print(test)
# print(type(test))
# print(test.shape)

# raise ValueError
df_test = df.iloc[test]
df_train = df.iloc[train]


df_test = df_test.sample(frac=1)
df_train = df_train.sample(frac=1)


print(df_test)

print("------------")

print(df_train)

# raise ValueError


y_true = df_test[target]
df_test = df_test.drop(columns=[target])

af = AutoFeaturizer(
    cache_src="./features_express.json", preset="express", guess_oxistates=True
)
# af = AutoFeaturizer(cache_src="./features_debug.json", preset="debug", guess_oxistates=True)
dc = DataCleaner(
    **{
        "max_na_frac": 0.01,
        "feature_na_method": "mean",
        "na_method_fit": "drop",
        "na_method_transform": "mean",
    }
)
fr = FeatureReducer(reducers=("tree",), tree_importance_percentile=0.99)


# config = {"n_estimators": 500}
# ml = SinglePipelineAdaptor(regressor=RandomForestRegressor(**config), classifier=RandomForestClassifier(**config))
config = {
    "max_time_mins": 30,
    "max_eval_time_mins": 5,
    "population_size": 20,
    "memory": "auto",
    "n_jobs": 8,
    "verbosity": 3,
}
ml = TPOTAdaptor(**config)

# af.fit_transform(df, target)

# df_train = af.fit_transform(df_train, target)
# df_train = dc.fit_transform(df_train, target)
# df_train = fr.fit_transform(df_train, target)
# ml.fit(df_train, target)
#
#
# df_test = af.transform(df_test, target)
# df_test = dc.transform(df_test, target)
# df_test = fr.transform(df_test, target)
# df_test = ml.predict(df_test, target)

pipe = MatPipe(autofeaturizer=af, cleaner=dc, reducer=fr, learner=ml)


# returned_dfs = pipe.benchmark(df, target, kfold=kf, cache=True, fold_subset=0)


pipe.fit(df_train, target)
df_test = pipe.predict(df_test, target)

y_pred = df_test[target + " predicted"]
print("ROC SCORE:", roc_auc_score(y_true, y_pred))
