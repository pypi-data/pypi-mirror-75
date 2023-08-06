#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


class Builder(Dict):
    __root__ = None

    def __init__(self, *args, **kwargs):
        super(Builder, self).__init__(*args, **kwargs)
        if self.__root__ is None:
            pass
        else:
            self[self.__root__] = Builder()

    def __getattr__(self, *args, **kwargs):
        name = args[0]
        return self.__setvalue(name)

    def __setvalue(self, name):
        self = self

        def foo(*args):
            if len(args) == 1:
                value = args[0]
                if self.__root__ is None:
                    self[name] = value
                else:
                    self[self.__root__][name] = value
            return self

        return foo


class Metadata(object):
    def withInput(self):
        if self.get("input") is None:
            self["input"] = Builder()

        return self

    def withInputData(self, value):
        self.withInput()
        if self["input"].get("data") is None:
            self["input"].data(Builder())
        if self["input"]["data"].get("data") is None:
            self["input"]["data"]["data"] = []
        self["input"]["data"]["data"].append(value)
        return self

    def withOutput(self):
        if self.get("output") is None:
            self["output"] = Builder()
        return self

    def withOutputData(self, value):
        self.withOutput()
        if self["output"].get("data") is None:
            self["output"]["data"] = []
        self["output"]["data"].append(value)
        return self

    def withOutputModel(self, value):
        self.withOutput()
        if self["output"].get("model") is None:
            self["output"]["model"] = []
        self["output"]["model"].append(value)
        return self


class DataIoBuilder(Builder, Metadata):
    pass


class HeteroFeatureBinninBuilder(Builder, Metadata):
    pass


class EvaluationBinninBuilder(Builder, Metadata):
    pass


class HeteroFeatureSelectionBuilder(Builder, Metadata):
    def withInputIsometricModel(self, value):
        self.withInput()
        if self["input"].get("isometric_model") is None:
            self["input"]["isometric_model"] = []
        self["input"]["isometric_model"].append(value)
        return self


class ComponentBuilder(Builder):
    __root__ = "components"


class InitiatorBuilder(Builder):

    def __init__(self, *args, **kwargs):
        super(InitiatorBuilder, self).__init__(*args, **kwargs)
        self["role"] = None
        self["party_id"] = None


class JobParameterBuilder(Builder):
    def __init__(self, *args, **kwargs):
        super(JobParameterBuilder, self).__init__(*args, **kwargs)
        self["work_mode"] = None


class AlgorithmParameterBuilder(Builder):
    pass


class RoleParameterBuilder(Builder):
    pass


class HostBuilder(Builder):
    def __init__(self, *args, **kwargs):
        super(HostBuilder, self).__init__(*args, **kwargs)
        self["args"] = Builder()
        self["args"]["data"] = Builder()
        self["args"]["data"]["train_data"] = []

        self["dataio_0"] = Builder()
        self["dataio_0"]["with_label"] = []
        self["dataio_0"]["output_format"] = []

    def train_data(self, value):
        self["args"]["data"]["train_data"].append(value)
        return self

    def with_label(self, value):
        self["dataio_0"]["with_label"].append(value)
        return self

    def output_format(self, value):
        self["dataio_0"]["output_format"].append(value)
        return self


class GuestBuilder(HostBuilder):
    def __init__(self, *args, **kwargs):
        super(GuestBuilder, self).__init__(*args, **kwargs)
        self["dataio_0"]["label_name"] = []
        self["dataio_0"]["label_type"] = []

    def label_name(self, value):
        self["dataio_0"]["label_name"].append(value)
        return self

    def label_type(self, value):
        self["dataio_0"]["label_type"].append(value)
        return self


class RoleBuilder(Builder):
    def __init__(self, *args, **kwargs):
        super(RoleBuilder, self).__init__(*args, **kwargs)
        self["guest"] = []
        self["host"] = []
        self["arbiter"] = []

    def guest(self, value):
        self["guest"].append(value)
        return self

    def host(self, value):
        self["host"].append(value)
        return self

    def arbiter(self, value):
        self["arbiter"].append(value)
        return self


class HeteroLrBuilder(Builder):

    def __init__(self, *args, **kwargs):
        super(HeteroLrBuilder, self).__init__(*args, **kwargs)
        self["penalty"] = None
        self["optimizer"] = None
        self["eps"] = None
        self["alpha"] = None
        self["max_iter"] = None
        self["converge_func"] = None
        self["batch_size"] = None
        self["learning_rate"] = None
        self["init_param"] = Builder()
        self["init_param"]["init_method"] = None

    def init_method(self, value):
        self["init_param"]["init_method"] = value
        return self


if __name__ == '__main__':
    configObj = Builder(). \
        initiator(
        InitiatorBuilder()
            .role("guest")
            .party_id(10000)
    ). \
        job_parameters(
        JobParameterBuilder()
            .work_mode(1)
    ). \
        role(
        RoleBuilder()
            .guest(10000)
            .host(9999)
            .arbiter(9999)
    ). \
        role_parameters(
        RoleParameterBuilder()
            .guest(
            GuestBuilder()
                .args()
                .data()
                .train_data(
                Builder()
                    .name("breast_b")
                    .namespace("fate_flow_test_breast")
            ).dataio_0()
                .with_label(True)
                .label_name("y")
                .label_type("int")
                .output_format("dense")
        ).host(
            HostBuilder().args()
                .data()
                .train_data(
                Builder()
                    .name("breast_a")
                    .namespace("fate_flow_test_breast")
            ).dataio_0()
                .with_label(False)
                .output_format("dense")
        )
    ). \
        algorithm_parameters(
        AlgorithmParameterBuilder()
            .hetero_lr_0(
            HeteroLrBuilder()
                .penalty("L2")
                .optimizer("rmsprop")
                .eps(1e-5)
                .alpha(0.01)
                .max_iter(3)
                .converge_func("diff")
                .batch_size(320)
                .learning_rate(0.15)
                .init_param().init_method("random_uniform")
        )
    )

    print(json.dumps(configObj, default=lambda o: o.__dict__,
                     indent=2, ensure_ascii=False))
    fmtObj = ComponentBuilder().dataio_0(
        DataIoBuilder()
        .module("DataIO")
        .withInputData("args.train_data")
        .withOutputData("train")
        .withOutputModel("dataio")
        .need_deploy(True)
    ).hetero_feature_binning_0(
        HeteroFeatureBinninBuilder()
        .module("HeteroFeatureBinning")
        .withInputData("hetero_feature_selection_0.eval")
        .withOutputData("train")
        .withOutputModel("hetero_feature_binning")
    ).hetero_feature_selection_0(
        HeteroFeatureSelectionBuilder()
        .module("HeteroFeatureSelection")
        .withInputData("hetero_feature_binning_0.train")
        .withInputIsometricModel("hetero_feature_binning_0.hetero_feature_binning")
        .withOutputData("eval")
        .withOutputModel("selected")
    ).evaluation_0(
        EvaluationBinninBuilder().module("Evaluation")
        .withInputData("hetero_feature_selection_0.eval")
        .withOutputData("evaluate")
    )
    print(json.dumps(fmtObj, default=lambda o: o.__dict__,
                     indent=2, ensure_ascii=False))

    data_io = ComponentBuilder().with_name('dataio_0').with_module(
        'DataIO').with_input_data('arg.train_data').with_output_data('train').with_output_model(
        'dataio').with_need_deploy(True).build()

    hetero_feature_selection = ComponentBuilder().with_name('hetero_feature_selection_0').with_module(
        'HeteroFeatureSelection').with_input_data('hetero_feature_binning_0.train').with_output_data(
        'eval').with_output_model('selected').with_input_isometric_model('hetero_feature_binning_0.hetero_feature_binning').build()

    hetero_feature_binning = ComponentBuilder().with_name('hetero_feature_binning_0').with_module(
        'HeteroFeatureBinning').with_input_data('hetero_feature_selection_0.eval').with_output_data(
        'train').with_output_model("hetero_feature_binning").build()

    evaluation = ComponentBuilder.with_name('evaluation_0').with_module(
        'Evaluation').with_input_data('hetero_feature_selection_0.eval').with_output_data('evaluate').build()

    pipline = PiplineBuilder().with_components(
        data_io, hetero_feature_selection, hetero_feature_binning, evaluation).build()
