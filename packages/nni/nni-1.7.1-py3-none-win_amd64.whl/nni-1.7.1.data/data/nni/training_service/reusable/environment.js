'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const log_1 = require("../../common/log");
const webCommandChannel_1 = require("./channels/webCommandChannel");
class EnvironmentInformation {
    constructor(id, jobName, jobId) {
        this.isIdle = false;
        this.isAlive = true;
        this.status = "UNKNOWN";
        this.trackingUrl = "";
        this.workingFolder = "";
        this.runnerWorkingFolder = "";
        this.command = "";
        this.nodeCount = 1;
        this.gpuSummary = new Map();
        this.log = log_1.getLogger();
        this.id = id;
        this.jobName = jobName;
        this.jobId = jobId ? jobId : jobName;
        this.nodes = new Map();
    }
    setFinalStatus(status) {
        switch (status) {
            case 'WAITING':
            case 'SUCCEEDED':
            case 'FAILED':
            case 'USER_CANCELED':
                this.status = status;
                break;
            default:
                this.log.error(`Environment: job ${this.jobId} set an invalid final state ${status}.`);
                break;
        }
    }
}
exports.EnvironmentInformation = EnvironmentInformation;
class EnvironmentService {
    getCommandChannel(commandEmitter) {
        return new webCommandChannel_1.WebCommandChannel(commandEmitter);
    }
    createEnviornmentInfomation(envId, envName) {
        return new EnvironmentInformation(envId, envName);
    }
}
exports.EnvironmentService = EnvironmentService;
class NodeInfomation {
    constructor(id) {
        this.status = "UNKNOWN";
        this.id = id;
    }
}
exports.NodeInfomation = NodeInfomation;
class RunnerSettings {
    constructor() {
        this.experimentId = "";
        this.platform = "";
        this.nniManagerIP = "";
        this.nniManagerPort = 8081;
        this.nniManagerVersion = "";
        this.logCollection = "none";
        this.command = "";
        this.enableGpuCollector = false;
        this.commandChannel = "file";
    }
}
exports.RunnerSettings = RunnerSettings;
