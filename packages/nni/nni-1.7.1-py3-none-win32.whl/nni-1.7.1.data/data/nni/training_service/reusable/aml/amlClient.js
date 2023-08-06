'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const ts_deferred_1 = require("ts-deferred");
const python_shell_1 = require("python-shell");
class AMLClient {
    constructor(subscriptionId, resourceGroup, workspaceName, experimentId, computeTarget, image, scriptName, codeDir) {
        this.subscriptionId = subscriptionId;
        this.resourceGroup = resourceGroup;
        this.workspaceName = workspaceName;
        this.experimentId = experimentId;
        this.image = image;
        this.scriptName = scriptName;
        this.codeDir = codeDir;
        this.computeTarget = computeTarget;
    }
    submit() {
        const deferred = new ts_deferred_1.Deferred();
        this.pythonShellClient = new python_shell_1.PythonShell('amlUtil.py', {
            scriptPath: './config/aml',
            pythonOptions: ['-u'],
            args: [
                '--subscription_id', this.subscriptionId,
                '--resource_group', this.resourceGroup,
                '--workspace_name', this.workspaceName,
                '--compute_target', this.computeTarget,
                '--docker_image', this.image,
                '--experiment_name', `nni_exp_${this.experimentId}`,
                '--script_dir', this.codeDir,
                '--script_name', this.scriptName
            ]
        });
        this.pythonShellClient.on('message', function (envId) {
            deferred.resolve(envId);
        });
        return deferred.promise;
    }
    stop() {
        if (this.pythonShellClient === undefined) {
            throw Error('python shell client not initialized!');
        }
        this.pythonShellClient.send('stop');
    }
    getTrackingUrl() {
        const deferred = new ts_deferred_1.Deferred();
        if (this.pythonShellClient === undefined) {
            throw Error('python shell client not initialized!');
        }
        this.pythonShellClient.send('tracking_url');
        let trackingUrl = '';
        this.pythonShellClient.on('message', function (status) {
            const items = status.split(':');
            if (items[0] === 'tracking_url') {
                trackingUrl = items.splice(1, items.length).join('');
            }
            deferred.resolve(trackingUrl);
        });
        return deferred.promise;
    }
    updateStatus(oldStatus) {
        const deferred = new ts_deferred_1.Deferred();
        if (this.pythonShellClient === undefined) {
            throw Error('python shell client not initialized!');
        }
        let newStatus = oldStatus;
        this.pythonShellClient.send('update_status');
        this.pythonShellClient.on('message', function (status) {
            const items = status.split(':');
            if (items[0] === 'status') {
                newStatus = items.splice(1, items.length).join('');
            }
            deferred.resolve(newStatus);
        });
        return deferred.promise;
    }
    sendCommand(message) {
        if (this.pythonShellClient === undefined) {
            throw Error('python shell client not initialized!');
        }
        this.pythonShellClient.send(`command:${message}`);
    }
    receiveCommand() {
        const deferred = new ts_deferred_1.Deferred();
        if (this.pythonShellClient === undefined) {
            throw Error('python shell client not initialized!');
        }
        this.pythonShellClient.send('receive');
        this.pythonShellClient.on('message', function (command) {
            const items = command.split(':');
            if (items[0] === 'receive') {
                deferred.resolve(JSON.parse(command.slice(8)));
            }
        });
        return deferred.promise;
    }
}
exports.AMLClient = AMLClient;
