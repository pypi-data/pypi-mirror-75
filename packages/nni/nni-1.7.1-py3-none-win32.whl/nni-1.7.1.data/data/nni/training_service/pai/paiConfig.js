'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
class PAIClusterConfig {
    constructor(userName, host, passWord, token, reuse) {
        this.userName = userName;
        this.passWord = passWord;
        this.host = host;
        this.token = token;
        this.reuse = reuse;
    }
}
exports.PAIClusterConfig = PAIClusterConfig;
class PAITrialJobDetail {
    constructor(id, status, paiJobName, submitTime, workingDirectory, form, logPath) {
        this.id = id;
        this.status = status;
        this.paiJobName = paiJobName;
        this.submitTime = submitTime;
        this.workingDirectory = workingDirectory;
        this.form = form;
        this.tags = [];
        this.logPath = logPath;
    }
}
exports.PAITrialJobDetail = PAITrialJobDetail;
