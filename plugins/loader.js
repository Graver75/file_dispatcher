/**
 * Script going through the directories, find React components
 * and exports them
 */
const PLUGINS_PATH = __dirname;
const COMPONENT_TYPES = [
  'NodeComponent'
];

const path = require('path');
const fs = require('fs');

const readDir = (path) => {
    return new Promise((resolve, reject) => {
        fs.readdir(path, (err, files) => {
            if (err) {
                return reject(err)
            }
            resolve(files.map(getAbsolutePath(path)))
        })
    })
};
const getAbsolutePath = (filePath) => {
    return (name) => {
        return path.resolve(filePath, name)
    }
};
const isPluginDirectory = (fileName) => {
    return /plugin$/.test(fileName)
};
const isPluginComponent = (fileName) => {
    fileName = fileName.split(path.sep).pop();
    return COMPONENT_TYPES.includes(fileName.replace(/\.[^/.]+$/, ""))
};
const getPluginsDirs = async (rootDir) => {
  let dirs = [];
  let files = await readDir(rootDir);
  for (let file of files) {
      if (file[0] !== '.') {
          let filePath = path.resolve(rootDir, file);
          let stat = await new Promise((resolve, reject) => {
              fs.stat(filePath, (err, fd) => {
                  if (err) {
                      return reject(err)
                  }
                  resolve(fd)
              });
          });
          if (stat.isDirectory() && isPluginDirectory(filePath)) {
              dirs.push(filePath)
          }
      }
  }
  return dirs
};
const iterThroughDirs = function* (paths) {
    for (let path of paths) {
        yield readDir(path)
    }
};
const getComponents = async () => {
    let iter = iterThroughDirs(await getPluginsDirs(PLUGINS_PATH));
    let components = [];
    for (let filesAwaited of iter) {
        let fileNames = await filesAwaited;
        for (let fileName of fileNames) {
            if (isPluginComponent(fileName)) {
                components.push(fileName)
            }
        }
    }
    return components
};

module.exports = new Promise((resolve, reject) => {
    (async() => {
        resolve(getComponents())
    })()
});