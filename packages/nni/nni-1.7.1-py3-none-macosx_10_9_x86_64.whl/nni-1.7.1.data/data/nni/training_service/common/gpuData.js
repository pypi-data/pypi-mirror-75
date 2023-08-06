'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
class GPUInfo {
    constructor(activeProcessNum, gpuMemUtil, gpuUtil, index, gpuMemTotal, gpuMemFree, gpuMemUsed, gpuType) {
        this.activeProcessNum = activeProcessNum;
        this.gpuMemUtil = gpuMemUtil;
        this.gpuUtil = gpuUtil;
        this.index = index;
        this.gpuMemTotal = gpuMemTotal;
        this.gpuMemFree = gpuMemFree;
        this.gpuMemUsed = gpuMemUsed;
        this.gpuType = gpuType;
    }
}
exports.GPUInfo = GPUInfo;
class GPUSummary {
    constructor(gpuCount, timestamp, gpuInfos) {
        this.gpuCount = gpuCount;
        this.timestamp = timestamp;
        this.gpuInfos = gpuInfos;
    }
}
exports.GPUSummary = GPUSummary;
exports.GPU_INFO_COLLECTOR_FORMAT_WINDOWS = `
$env:METRIC_OUTPUT_DIR="{0}"
$app = Start-Process "python" -ArgumentList "-m nni_gpu_tool.gpu_metrics_collector" -passthru -NoNewWindow
Write $app.ID | Out-File {1} -NoNewline -encoding utf8
`;
