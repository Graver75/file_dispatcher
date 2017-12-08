import prefetch from './prefetch';

export default class Ajax {
    static getNodes() {
        return prefetch('/api/nodes')
    }
    static getFiles(id) {
        return prefetch(`/api/nodes/${id}/files`)
    }
    static getNodeInfo(id) {
        return id ? prefetch(`/api/nodes/${id}`) : prefetch(`/api/info`)
    }
    static getFileInfo(id) {
        return prefetch(`/api/files/${id}`)
    }
    static getFile(id) {
        return prefetch(`/api/files/${id}/download`)
    }
}