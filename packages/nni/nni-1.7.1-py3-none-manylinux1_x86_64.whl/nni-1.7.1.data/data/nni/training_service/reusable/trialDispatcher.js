'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const events_1 = require("events");
const fs = require("fs");
const path = require("path");
const typescript_string_operations_1 = require("typescript-string-operations");
const component = require("../../common/component");
const experimentStartupInfo_1 = require("../../common/experimentStartupInfo");
const log_1 = require("../../common/log");
const utils_1 = require("../../common/utils");
const commands_1 = require("../../core/commands");
const containerJobData_1 = require("../common/containerJobData");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const util_1 = require("../common/util");
const environment_1 = require("./environment");
const mountedStorageService_1 = require("./storages/mountedStorageService");
const storageService_1 = require("./storageService");
const trial_1 = require("./trial");
let TrialDispatcher = class TrialDispatcher {
    constructor() {
        this.NNI_METRICS_PATTERN = `NNISDK_MEb'(?<metrics>.*?)'`;
        this.isDeveloping = false;
        this.stopping = false;
        this.enableVersionCheck = true;
        this.log = log_1.getLogger();
        this.trials = new Map();
        this.environments = new Map();
        this.metricsEmitter = new events_1.EventEmitter();
        this.experimentId = experimentStartupInfo_1.getExperimentId();
        this.experimentRootDir = utils_1.getExperimentRootDir();
        this.runnerSettings = new environment_1.RunnerSettings();
        this.runnerSettings.experimentId = this.experimentId;
        this.runnerSettings.platform = experimentStartupInfo_1.getPlatform();
        const logLevel = utils_1.getLogLevel();
        this.log.debug(`current folder ${__dirname}`);
        if (logLevel == "debug" && (fs.existsSync("../../../src/nni_manager") || __dirname.endsWith("src\\nni_manager\\dist\\training_service\\reusable"))) {
            this.log.debug("log level is debug, and exist code folder, so set to developing mode.");
            this.isDeveloping = true;
            this.runnerSettings.enableGpuCollector = true;
        }
    }
    async listTrialJobs() {
        const trials = [];
        for (const key of this.trials.keys()) {
            trials.push(await this.getTrialJob(key));
        }
        return trials;
    }
    async getTrialJob(trialJobId) {
        const trial = this.trials.get(trialJobId);
        if (trial === undefined) {
            throw new Error(`trial job ${trialJobId} not found`);
        }
        return trial;
    }
    async submitTrialJob(form) {
        if (this.trialConfig === undefined) {
            throw new Error(`trialConfig not initialized!`);
        }
        const trialId = utils_1.uniqueString(5);
        const environmentService = component.get(environment_1.EnvironmentService);
        let trialWorkingFolder = "";
        if (environmentService.hasStorageService) {
            const storageService = component.get(storageService_1.StorageService);
            trialWorkingFolder = storageService.joinPath('trials', trialId);
        }
        const trialJobDetail = new trial_1.TrialDetail(trialId, "WAITING", Date.now(), trialWorkingFolder, form);
        this.trials.set(trialId, trialJobDetail);
        return trialJobDetail;
    }
    async updateTrialJob(trialJobId, form) {
        const trialDetail = await this.getTrialJob(trialJobId);
        const environment = trialDetail.environment;
        if (environment === undefined) {
            throw new Error(`TrialDispatcher: trial ${trialJobId}'s env shouldn't be undefined in updateTrialJob.`);
        }
        if (this.commandChannel === undefined) {
            throw new Error(`TrialDispatcher: commandChannel shouldn't be undefined in updateTrialJob.`);
        }
        const message = {
            "trialId": trialJobId,
            "parameters": form.hyperParameters,
        };
        await this.commandChannel.sendCommand(environment, commands_1.SEND_TRIAL_JOB_PARAMETER, message);
        return trialDetail;
    }
    async cancelTrialJob(trialJobId, isEarlyStopped) {
        if (this.commandChannel === undefined) {
            throw new Error(`TrialDispatcher: commandChannel shouldn't be undefined in cancelTrialJob.`);
        }
        const trial = await this.getTrialJob(trialJobId);
        switch (trial.status) {
            case "RUNNING":
            case "WAITING":
            case "UNKNOWN":
                {
                    const environment = trial.environment;
                    if (environment) {
                        await this.commandChannel.sendCommand(environment, commands_1.KILL_TRIAL_JOB, trial.id);
                        trial.isEarlyStopped = isEarlyStopped;
                        trial.status = trial.isEarlyStopped === true ?
                            'EARLY_STOPPED' : 'USER_CANCELED';
                        this.releaseEnvironment(trial);
                    }
                }
                break;
        }
    }
    async run() {
        const environmentService = component.get(environment_1.EnvironmentService);
        this.commandEmitter = new events_1.EventEmitter();
        this.commandChannel = environmentService.getCommandChannel(this.commandEmitter);
        if (this.runnerSettings.nniManagerIP === "" || this.runnerSettings.nniManagerIP === null) {
            this.runnerSettings.nniManagerIP = utils_1.getIPV4Address();
        }
        this.runnerSettings.nniManagerPort = experimentStartupInfo_1.getBasePort() + 1;
        this.runnerSettings.commandChannel = this.commandChannel.channelName;
        await this.commandChannel.config("MetricEmitter", this.metricsEmitter);
        this.commandEmitter.on("command", (command) => {
            this.handleCommand(command).catch((err) => {
                this.log.error(`TrialDispatcher: error on handle env ${command.environment.id} command: ${command.command}, data: ${command.data}, error: ${err}`);
            });
        });
        await this.commandChannel.start();
        this.log.info(`TrialDispatcher: started channel: ${this.commandChannel.constructor.name}`);
        if (this.trialConfig === undefined) {
            throw new Error(`trial config shouldn't be undefined in run()`);
        }
        this.log.info(`TrialDispatcher: copying code and settings.`);
        let storageService;
        if (environmentService.hasStorageService) {
            this.log.debug(`TrialDispatcher: use existing storage service.`);
            storageService = component.get(storageService_1.StorageService);
        }
        else {
            this.log.debug(`TrialDispatcher: create temp storage service to temp folder.`);
            storageService = new mountedStorageService_1.MountedStorageService();
            const environmentLocalTempFolder = path.join(this.experimentRootDir, this.experimentId, "environment-temp");
            storageService.initialize(this.trialConfig.codeDir, environmentLocalTempFolder);
        }
        const codeDir = path.resolve(this.trialConfig.codeDir);
        const envDir = storageService.joinPath("envs");
        const codeFileName = await storageService.copyDirectory(codeDir, envDir, true);
        storageService.rename(codeFileName, "nni-code.tar.gz");
        const installFileName = storageService.joinPath(envDir, 'install_nni.sh');
        await storageService.save(containerJobData_1.CONTAINER_INSTALL_NNI_SHELL_FORMAT, installFileName);
        const runnerSettings = storageService.joinPath(envDir, "settings.json");
        await storageService.save(JSON.stringify(this.runnerSettings), runnerSettings);
        if (this.isDeveloping) {
            let trialToolsPath = path.join(__dirname, "../../../../../tools/nni_trial_tool");
            if (false === fs.existsSync(trialToolsPath)) {
                trialToolsPath = path.join(__dirname, "..\\..\\..\\..\\..\\tools\\nni_trial_tool");
            }
            await storageService.copyDirectory(trialToolsPath, envDir, true);
        }
        this.log.info(`TrialDispatcher: run loop started.`);
        await Promise.all([
            this.environmentMaintenanceLoop(),
            this.trialManagementLoop(),
            this.commandChannel.run(),
        ]);
    }
    addTrialJobMetricListener(listener) {
        this.metricsEmitter.on('metric', listener);
    }
    removeTrialJobMetricListener(listener) {
        this.metricsEmitter.off('metric', listener);
    }
    get isMultiPhaseJobSupported() {
        return true;
    }
    async setClusterMetadata(key, value) {
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.NNI_MANAGER_IP:
                this.runnerSettings.nniManagerIP = JSON.parse(value).nniManagerIp;
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.VERSION_CHECK:
                this.enableVersionCheck = (value === 'true' || value === 'True');
                this.runnerSettings.nniManagerVersion = this.enableVersionCheck ? await utils_1.getVersion() : '';
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.LOG_COLLECTION:
                this.runnerSettings.logCollection = value;
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                this.trialConfig = JSON.parse(value);
                this.runnerSettings.command = this.trialConfig.command;
                await util_1.validateCodeDir(this.trialConfig.codeDir);
                break;
        }
        const environmentService = component.get(environment_1.EnvironmentService);
        await environmentService.config(key, value);
    }
    getClusterMetadata(_key) {
        throw new Error('Not implemented!');
    }
    async cleanUp() {
        if (this.commandChannel === undefined) {
            throw new Error(`TrialDispatcher: commandChannel shouldn't be undefined in cleanUp.`);
        }
        if (this.commandEmitter === undefined) {
            throw new Error(`TrialDispatcher: commandEmitter shouldn't be undefined in cleanUp.`);
        }
        this.stopping = true;
        const environmentService = component.get(environment_1.EnvironmentService);
        const environments = [...this.environments.values()];
        for (let index = 0; index < environments.length; index++) {
            const environment = environments[index];
            if (environment.isAlive === true) {
                this.log.info(`stopping environment ${environment.id}...`);
                await environmentService.stopEnvironment(environment);
                await this.commandChannel.close(environment);
                this.log.info(`stopped environment ${environment.id}.`);
            }
        }
        this.commandEmitter.off("command", this.handleCommand);
        await this.commandChannel.stop();
    }
    async environmentMaintenanceLoop() {
        if (this.commandChannel === undefined) {
            throw new Error(`TrialDispatcher: commandChannel shouldn't be undefined in environmentMaintenanceLoop.`);
        }
        const environmentService = component.get(environment_1.EnvironmentService);
        while (!this.stopping) {
            const environments = [];
            for (const environment of this.environments.values()) {
                if (environment.isAlive === true) {
                    environments.push(environment);
                }
                else {
                    await this.commandChannel.close(environment);
                }
            }
            await environmentService.refreshEnvironmentsStatus(environments);
            environments.forEach((environment) => {
                const oldIsAlive = environment.isAlive;
                switch (environment.status) {
                    case 'WAITING':
                    case 'RUNNING':
                    case 'UNKNOWN':
                        environment.isAlive = true;
                        break;
                    default:
                        environment.isAlive = false;
                        break;
                }
                if (oldIsAlive !== environment.isAlive) {
                    this.log.debug(`set environment ${environment.id} isAlive from ${oldIsAlive} to ${environment.isAlive} due to status is ${environment.status}.`);
                }
            });
            await utils_1.delay(5000);
        }
    }
    async trialManagementLoop() {
        if (this.commandChannel === undefined) {
            throw new Error(`TrialDispatcher: commandChannel shouldn't be undefined in trialManagementLoop.`);
        }
        while (!this.stopping) {
            await utils_1.delay(2000);
            const toRefreshedTrials = [];
            for (const trial of this.trials.values()) {
                if (trial.status === "RUNNING" || trial.status === "WAITING" || trial.status === "UNKNOWN") {
                    toRefreshedTrials.push(trial);
                }
            }
            if (toRefreshedTrials.length == 0) {
                continue;
            }
            const waitingTrials = [];
            let liveTrialsCount = 0;
            for (const trial of toRefreshedTrials) {
                const currentStatus = trial.status;
                switch (currentStatus) {
                    case "RUNNING":
                        {
                            const environment = trial.environment;
                            if (environment === undefined) {
                                this.log.error(`found running trial ${trial.id} has no environment, set trial to UNKNOWN.`);
                                trial.status = "UNKNOWN";
                                liveTrialsCount++;
                                continue;
                            }
                            const environmentStatus = environment.status;
                            if (trial.nodes.size > 0) {
                                const completedCount = trial.nodes.size;
                                let finalStatus = "SUCCEEDED";
                                let lastTimestamp;
                                this.log.debug(`found ${completedCount} completed trial node(s), nodeCount: ${environment.nodeCount}`);
                                if (environment.nodeCount > completedCount) {
                                    this.log.info(`stop partial completed trial ${trial.id}`);
                                    await this.commandChannel.sendCommand(environment, commands_1.KILL_TRIAL_JOB, trial.id);
                                }
                                for (const node of trial.nodes.values()) {
                                    if (node.status === "FAILED") {
                                        finalStatus = "FAILED";
                                    }
                                    if (node.endTime !== undefined) {
                                        if (lastTimestamp === undefined) {
                                            lastTimestamp = node.endTime;
                                        }
                                        else {
                                            lastTimestamp = Math.max(node.endTime, lastTimestamp);
                                        }
                                    }
                                }
                                trial.status = finalStatus;
                                if (lastTimestamp === undefined) {
                                    trial.endTime = lastTimestamp;
                                }
                                this.releaseEnvironment(trial);
                            }
                            else if (environmentStatus !== "RUNNING") {
                                this.log.error(`found running trial ${trial.id} on '${environment.jobId}' with '${environmentStatus}', set trial to environment status.`);
                                this.releaseEnvironment(trial);
                                trial.status = environmentStatus;
                            }
                            else {
                                liveTrialsCount++;
                            }
                        }
                        break;
                    case "WAITING":
                    case "UNKNOWN":
                        waitingTrials.push(trial);
                        liveTrialsCount++;
                        break;
                }
            }
            let liveEnvironmentsCount = 0;
            const idleEnvironments = [];
            this.environments.forEach((environment) => {
                if (environment.isAlive === true) {
                    liveEnvironmentsCount++;
                    if (environment.status === "RUNNING" && environment.isIdle) {
                        idleEnvironments.push(environment);
                    }
                }
            });
            while (idleEnvironments.length > 0 && waitingTrials.length > 0) {
                const trial = waitingTrials.shift();
                const idleEnvironment = idleEnvironments.shift();
                if (trial !== undefined && idleEnvironment != undefined) {
                    await this.assignEnvironment(trial, idleEnvironment);
                }
            }
            if (liveEnvironmentsCount < liveTrialsCount) {
                this.log.info(`request new environment, since live trials ${liveTrialsCount} ` +
                    `is more than live environments ${liveEnvironmentsCount}`);
                for (let index = 0; index < liveTrialsCount - liveEnvironmentsCount; index++) {
                    await this.requestEnvironment();
                }
            }
        }
    }
    async requestEnvironment() {
        if (this.commandChannel === undefined) {
            throw new Error(`TrialDispatcher: commandChannel shouldn't be undefined in requestEnvironment.`);
        }
        const environmentService = component.get(environment_1.EnvironmentService);
        const envId = utils_1.uniqueString(5);
        const envName = `nni_exp_${this.experimentId}_env_${envId}`;
        const environment = environmentService.createEnviornmentInfomation(envId, envName);
        environment.command = `sh ../install_nni.sh && python3 -m nni_trial_tool.trial_runner`;
        if (this.isDeveloping) {
            environment.command = "[ -d \"nni_trial_tool\" ] && echo \"nni_trial_tool exists already\" || (mkdir ./nni_trial_tool && tar -xof ../nni_trial_tool.tar.gz -C ./nni_trial_tool) && pip3 install websockets && " + environment.command;
        }
        environment.command = `mkdir -p envs/${envId} && cd envs/${envId} && ${environment.command}`;
        await environmentService.startEnvironment(environment);
        this.environments.set(environment.id, environment);
        if (environment.status === "FAILED") {
            environment.isIdle = false;
            environment.isAlive = false;
            throw new Error(`error on request environment ${environment.jobId}, please check log for more details.`);
        }
        else {
            environment.isIdle = true;
            environment.isAlive = true;
        }
        await this.commandChannel.open(environment);
        this.log.info(`requested environment ${environment.id} and job id is ${environment.jobId}.`);
    }
    async assignEnvironment(trial, environment) {
        if (this.commandChannel === undefined) {
            throw new Error(`TrialDispatcher: commandChannel shouldn't be undefined in assignEnvironment.`);
        }
        if (trial.environment) {
            throw new Error(`trial ${trial.id} has assigned environment ${trial.environment.id} already, not assign to ${environment.id}!`);
        }
        if (environment.isIdle == false) {
            throw new Error(`environment ${environment.id} is not idle, and cannot be assigned again!`);
        }
        this.log.info(`assigning environment ${environment.id} to trial ${trial.id}.`);
        environment.isIdle = false;
        trial.environment = environment;
        trial.settings = {
            trialId: trial.id,
            sequenceId: trial.form.sequenceId,
            parameter: trial.form.hyperParameters,
        };
        trial.startTime = Date.now();
        trial.status = "RUNNING";
        await this.commandChannel.sendCommand(trial.environment, commands_1.NEW_TRIAL_JOB, trial.settings);
    }
    releaseEnvironment(trial) {
        if (!trial.environment) {
            throw new Error(`environment is not assigned to trial ${trial.id}, and cannot be released!`);
        }
        if (trial.environment.isIdle) {
            throw new Error(`environment ${trial.environment.id} is idle already!`);
        }
        trial.environment.isIdle = true;
        trial.environment = undefined;
    }
    async handleMetricData(trialId, data) {
        if (Array.isArray(data)) {
            for (const subItem of data) {
                this.metricsEmitter.emit('metric', {
                    id: trialId,
                    data: subItem
                });
            }
        }
        else {
            this.metricsEmitter.emit('metric', {
                id: trialId,
                data: data
            });
        }
    }
    async handleStdout(commandData) {
        const metricPattern = /NNISDK_MEb'(?<metrics>.*a?)'$/gm;
        const trialLogDir = path.join(utils_1.getExperimentRootDir(), 'trials', commandData["trial"]);
        utils_1.mkDirPSync(trialLogDir);
        const trialLogPath = path.join(trialLogDir, 'stdout_log_collection.log');
        try {
            let skipLogging = false;
            if (commandData["tag"] === 'trial' && commandData["msg"] !== undefined) {
                const message = commandData["msg"];
                let metricsContent = metricPattern.exec(message);
                while (metricsContent && metricsContent.groups) {
                    const key = 'metrics';
                    const data = metricsContent.groups[key];
                    await this.handleMetricData(commandData["trial"], data);
                    metricsContent = metricPattern.exec(message);
                    skipLogging = true;
                }
            }
            if (!skipLogging) {
                const writeStream = fs.createWriteStream(trialLogPath, {
                    flags: 'a+',
                    encoding: 'utf8',
                    autoClose: true
                });
                writeStream.write(typescript_string_operations_1.String.Format('{0}\n', commandData["msg"]));
                writeStream.end();
            }
        }
        catch (err) {
            this.log.error(`TrialDispatcher: handleStdout error: ${err}`);
        }
    }
    async handleCommand(command) {
        this.log.debug(`TrialDispatcher: env ${command.environment.id} received command ${command.command}, data: ${command.data}`);
        const environment = command.environment;
        const data = command.data;
        const nodeId = data["node"];
        switch (command.command) {
            case commands_1.REPORT_METRIC_DATA:
                this.log.error(`TrialDispatcher: TODO: not implement to handle direct REPORT_METRIC_DATA command yet.`);
                break;
            case commands_1.STDOUT:
                await this.handleStdout(data);
                break;
            case commands_1.INITIALIZED:
                {
                    const oldStatus = environment.status;
                    let isAllReady = true;
                    if (environment.nodeCount > 1) {
                        let node = environment.nodes.get(nodeId);
                        if (node === undefined) {
                            node = new environment_1.NodeInfomation(nodeId);
                            environment.nodes.set(nodeId, node);
                        }
                        const oldNodeStatus = node.status;
                        if (oldNodeStatus === "UNKNOWN" || oldNodeStatus === "WAITING") {
                            node.status = "RUNNING";
                        }
                        if (environment.nodes.size === environment.nodeCount) {
                            for (const node of environment.nodes.values()) {
                                if (node.status !== "RUNNING") {
                                    isAllReady = false;
                                    break;
                                }
                            }
                        }
                        else {
                            isAllReady = false;
                        }
                    }
                    if (isAllReady && oldStatus === "UNKNOWN") {
                        environment.status = "RUNNING";
                        this.log.info(`TrialDispatcher: env ${environment.id} received initialized message, old status: ${oldStatus}, new status: ${environment.status}.`);
                    }
                }
                break;
            case commands_1.VERSION_CHECK:
                {
                    if (this.enableVersionCheck) {
                        const checkResultSuccess = data["tag"] === 'VCSuccess' ? true : false;
                        if (checkResultSuccess) {
                            this.log.info(`TrialDispatcher: Version check in trialKeeper success!`);
                        }
                        else {
                            const errorMessage = `TrialDispatcher: Version check error, ${data["msg"]}!`;
                            this.log.error(errorMessage);
                        }
                    }
                }
                break;
            case commands_1.GPU_INFO:
                environment.gpuSummary.set(nodeId, (data));
                break;
            case commands_1.TRIAL_END:
                {
                    const trialId = data["trial"];
                    const trial = await this.getTrialJob(trialId);
                    const code = parseInt(data["code"]);
                    const timestamp = parseInt(data["time"]);
                    let exitStatus = "SUCCEEDED";
                    if (code !== 0) {
                        exitStatus = "FAILED";
                    }
                    let node = environment.nodes.get(nodeId);
                    if (node === undefined) {
                        node = new environment_1.NodeInfomation(nodeId);
                        trial.nodes.set(nodeId, node);
                    }
                    if (undefined === node) {
                        throw new Error("node is impossible to be undefined (see above code), but make eslint happy!");
                    }
                    node.status = exitStatus;
                    node.endTime = timestamp;
                }
                break;
        }
    }
};
TrialDispatcher = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], TrialDispatcher);
exports.TrialDispatcher = TrialDispatcher;
