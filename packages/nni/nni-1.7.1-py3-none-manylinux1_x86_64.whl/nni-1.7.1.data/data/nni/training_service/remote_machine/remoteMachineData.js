'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const shellExecutor_1 = require("./shellExecutor");
class RemoteMachineMeta {
    constructor() {
        this.ip = '';
        this.port = 22;
        this.username = '';
        this.passwd = '';
        this.useActiveGpu = false;
    }
}
exports.RemoteMachineMeta = RemoteMachineMeta;
function parseGpuIndices(gpuIndices) {
    if (gpuIndices !== undefined) {
        const indices = gpuIndices.split(',')
            .map((x) => parseInt(x, 10));
        if (indices.length > 0) {
            return new Set(indices);
        }
        else {
            throw new Error('gpuIndices can not be empty if specified.');
        }
    }
}
exports.parseGpuIndices = parseGpuIndices;
class RemoteCommandResult {
    constructor(stdout, stderr, exitCode) {
        this.stdout = stdout;
        this.stderr = stderr;
        this.exitCode = exitCode;
    }
}
exports.RemoteCommandResult = RemoteCommandResult;
class RemoteMachineTrialJobDetail {
    constructor(id, status, submitTime, workingDirectory, form) {
        this.id = id;
        this.status = status;
        this.submitTime = submitTime;
        this.workingDirectory = workingDirectory;
        this.form = form;
        this.tags = [];
        this.gpuIndices = [];
    }
}
exports.RemoteMachineTrialJobDetail = RemoteMachineTrialJobDetail;
class ExecutorManager {
    constructor(rmMeta) {
        this.executorMap = new Map();
        this.executors = [];
        this.rmMeta = rmMeta;
    }
    async getExecutor(id) {
        let isFound = false;
        let executor;
        if (this.executorMap.has(id)) {
            executor = this.executorMap.get(id);
            if (executor === undefined) {
                throw new Error("executor shouldn't be undefined before return!");
            }
            return executor;
        }
        for (const candidateExecutor of this.executors) {
            if (candidateExecutor.addUsage()) {
                isFound = true;
                executor = candidateExecutor;
                break;
            }
        }
        if (!isFound) {
            executor = await this.createShellExecutor();
        }
        if (executor === undefined) {
            throw new Error("executor shouldn't be undefined before set!");
        }
        this.executorMap.set(id, executor);
        return executor;
    }
    releaseAllExecutor() {
        this.executorMap.clear();
        for (const executor of this.executors) {
            executor.close();
        }
        this.executors = [];
    }
    releaseExecutor(id) {
        const executor = this.executorMap.get(id);
        if (executor === undefined) {
            throw new Error(`executor for ${id} is not found`);
        }
        executor.releaseUsage();
        this.executorMap.delete(id);
    }
    async createShellExecutor() {
        const executor = new shellExecutor_1.ShellExecutor();
        await executor.initialize(this.rmMeta);
        if (!executor.addUsage()) {
            throw new Error("failed to add usage on new created Executor! It's a wired bug!");
        }
        this.executors.push(executor);
        return executor;
    }
}
exports.ExecutorManager = ExecutorManager;
var ScheduleResultType;
(function (ScheduleResultType) {
    ScheduleResultType[ScheduleResultType["SUCCEED"] = 0] = "SUCCEED";
    ScheduleResultType[ScheduleResultType["TMP_NO_AVAILABLE_GPU"] = 1] = "TMP_NO_AVAILABLE_GPU";
    ScheduleResultType[ScheduleResultType["REQUIRE_EXCEED_TOTAL"] = 2] = "REQUIRE_EXCEED_TOTAL";
})(ScheduleResultType = exports.ScheduleResultType || (exports.ScheduleResultType = {}));
