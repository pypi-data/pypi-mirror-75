'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const cpp = require("child-process-promise");
const fs = require("fs");
const chai = require("chai");
const chaiAsPromised = require("chai-as-promised");
const shellExecutor_1 = require("../shellExecutor");
const utils_1 = require("../../../common/utils");
const LOCALFILE = 'localSshUTData';
const REMOTEFILE = 'remoteSshUTData';
const REMOTEFOLDER = 'remoteSshUTFolder';
async function copyFile(executor) {
    const remoteFullName = executor.joinPath(executor.getTempPath(), REMOTEFILE);
    await executor.copyFileToRemote(LOCALFILE, remoteFullName);
}
async function copyFileToRemoteLoop(executor) {
    const remoteFullName = executor.joinPath(executor.getTempPath(), REMOTEFILE);
    for (let i = 0; i < 3; i++) {
        await executor.copyFileToRemote(LOCALFILE, remoteFullName);
    }
}
async function getRemoteFileContentLoop(executor) {
    const remoteFullName = executor.joinPath(executor.getTempPath(), REMOTEFILE);
    for (let i = 0; i < 3; i++) {
        await executor.getRemoteFileContent(remoteFullName);
    }
}
describe('ShellExecutor test', () => {
    let skip = false;
    let rmMeta;
    try {
        rmMeta = JSON.parse(fs.readFileSync('../../.vscode/rminfo.json', 'utf8'));
        console.log(rmMeta);
    }
    catch (err) {
        console.log(`Please configure rminfo.json to enable remote machine test. ${err}`);
        skip = true;
    }
    before(async () => {
        chai.should();
        chai.use(chaiAsPromised);
        if (!fs.existsSync(LOCALFILE)) {
            await cpp.exec(`echo '1234' > ${LOCALFILE}`);
        }
        utils_1.prepareUnitTest();
    });
    after(() => {
        utils_1.cleanupUnitTest();
        fs.unlinkSync(LOCALFILE);
    });
    it('Test mkdir', async () => {
        if (skip) {
            return;
        }
        const executor = new shellExecutor_1.ShellExecutor();
        await executor.initialize(rmMeta);
        const remoteFullPath = executor.joinPath(executor.getTempPath(), REMOTEFOLDER);
        let result = await executor.createFolder(remoteFullPath, false);
        chai.expect(result).eq(true);
        const commandResult = await executor.executeScript("dir");
        chai.expect(commandResult.exitCode).eq(0);
        result = await executor.removeFolder(remoteFullPath);
        chai.expect(result).eq(true);
        await executor.close();
    });
    it('Test ShellExecutor', async () => {
        if (skip) {
            return;
        }
        const executor = new shellExecutor_1.ShellExecutor();
        await executor.initialize(rmMeta);
        await copyFile(executor);
        await copyFileToRemoteLoop(executor);
        await getRemoteFileContentLoop(executor);
        await executor.close();
    });
});
