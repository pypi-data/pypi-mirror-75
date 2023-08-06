'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const chai = require("chai");
const fs = require("fs");
const path = require("path");
const tar = require("tar");
const util_1 = require("../common/util");
const deleteFolderRecursive = (filePath) => {
    if (fs.existsSync(filePath)) {
        fs.readdirSync(filePath).forEach((file, index) => {
            const curPath = path.join(filePath, file);
            if (fs.lstatSync(curPath).isDirectory()) {
                deleteFolderRecursive(curPath);
            }
            else {
                fs.unlinkSync(curPath);
            }
        });
        fs.rmdirSync(filePath);
    }
};
describe('fileUtility', () => {
    const sourceDir = 'test-fileUtilityTestSource';
    const destDir = 'test-fileUtilityTestDest';
    beforeEach(() => {
        fs.mkdirSync(sourceDir);
        fs.writeFileSync(path.join(sourceDir, '.nniignore'), 'abc\nxyz');
        fs.writeFileSync(path.join(sourceDir, 'abc'), '123');
        fs.writeFileSync(path.join(sourceDir, 'abcd'), '1234');
        fs.mkdirSync(path.join(sourceDir, 'xyz'));
        fs.mkdirSync(path.join(sourceDir, 'xyy'));
        fs.mkdirSync(path.join(sourceDir, 'www'));
        fs.mkdirSync(path.join(sourceDir, 'xx'));
        fs.writeFileSync(path.join(sourceDir, 'xyy', '.nniignore'), 'qq');
        fs.writeFileSync(path.join(sourceDir, 'xyy', 'abc'), '123');
        fs.writeFileSync(path.join(sourceDir, 'xyy', 'qq'), '1234');
        fs.writeFileSync(path.join(sourceDir, 'xyy', 'pp'), '1234');
        fs.writeFileSync(path.join(sourceDir, 'www', '.nniignore'), 'pp');
        fs.writeFileSync(path.join(sourceDir, 'www', 'abc'), '123');
        fs.writeFileSync(path.join(sourceDir, 'www', 'qq'), '1234');
        fs.writeFileSync(path.join(sourceDir, 'www', 'pp'), '1234');
    });
    afterEach(() => {
        deleteFolderRecursive(sourceDir);
        deleteFolderRecursive(destDir);
        if (fs.existsSync(`${destDir}.tar`)) {
            fs.unlinkSync(`${destDir}.tar`);
        }
    });
    it('Test file copy', async () => {
        await util_1.execCopydir(sourceDir, destDir);
        const existFiles = [
            'abcd',
            'xyy',
            'xx',
            path.join('xyy', '.nniignore'),
            path.join('xyy', 'pp'),
            path.join('www', '.nniignore'),
            path.join('www', 'qq'),
        ];
        const notExistFiles = [
            'abc',
            'xyz',
            path.join('xyy', 'abc'),
            path.join('xyy', 'qq'),
            path.join('www', 'pp'),
            path.join('www', 'abc'),
        ];
        existFiles.forEach(d => assert.ok(fs.existsSync(path.join(destDir, d))));
        notExistFiles.forEach(d => assert.ok(!fs.existsSync(path.join(destDir, d))));
    });
    it('Test file copy without ignore', async () => {
        fs.unlinkSync(path.join(sourceDir, '.nniignore'));
        await util_1.execCopydir(sourceDir, destDir);
        assert.ok(fs.existsSync(path.join(destDir, 'abcd')));
        assert.ok(fs.existsSync(path.join(destDir, 'abc')));
        assert.ok(fs.existsSync(path.join(destDir, 'xyz')));
        assert.ok(fs.existsSync(path.join(destDir, 'xyy')));
        assert.ok(fs.existsSync(path.join(destDir, 'xx')));
    });
    it('Test tar file', async () => {
        const tarPath = `${destDir}.tar`;
        await util_1.tarAdd(tarPath, sourceDir);
        assert.ok(fs.existsSync(tarPath));
        fs.mkdirSync(destDir);
        tar.extract({
            file: tarPath,
            cwd: destDir,
            sync: true
        });
        assert.ok(fs.existsSync(path.join(destDir, 'abcd')));
        assert.ok(!fs.existsSync(path.join(destDir, 'abc')));
    });
    it('Validate code ok', async () => {
        assert.doesNotThrow(async () => util_1.validateCodeDir(sourceDir));
    });
    it('Validate code too many files', async () => {
        for (let i = 0; i < 2000; ++i)
            fs.writeFileSync(path.join(sourceDir, `${i}.txt`), 'a');
        try {
            await util_1.validateCodeDir(sourceDir);
        }
        catch (error) {
            chai.expect(error.message).to.contains('many files');
            return;
        }
        chai.expect.fail(null, null, 'Did not fail.');
    });
    it('Validate code too many files ok', async () => {
        for (let i = 0; i < 2000; ++i)
            fs.writeFileSync(path.join(sourceDir, `${i}.txt`), 'a');
        fs.writeFileSync(path.join(sourceDir, '.nniignore'), '*.txt');
        assert.doesNotThrow(async () => util_1.validateCodeDir(sourceDir));
    });
});
