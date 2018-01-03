/**
 * Script going through the directories, find React components
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
const removeExtension = (fileName) => {
    return fileName.replace(/\.[^/.]+$/, "")
};
const isPluginComponent = (fileName) => {
    return COMPONENT_TYPES.includes(getPluginComponentName(fileName))
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
const getPluginComponentName = (fileName) => {
    return removeExtension(fileName.split(path.sep).pop());
};
const iterThroughDirs = function* (paths) {
    for (let path of paths) {
        yield readDir(path)
    }
};
const definePluginComponent = (fileName, arrOfComponents) => {
    if (isPluginComponent(fileName)) {
        // TODO: optimize
        let componentName = getPluginComponentName(fileName);
        arrOfComponents[componentName].push(fileName)
    }
};
const getComponents = async () => {
    let iter = iterThroughDirs(await getPluginsDirs(PLUGINS_PATH));
    let components = {};
    COMPONENT_TYPES.forEach((elem) => {
        components[elem] = []
    });
    for (let filesAwaited of iter) {
        let fileNames = await filesAwaited;
        for (let fileName of fileNames) {
            if (isPluginComponent(fileName)) {
                definePluginComponent(fileName, components)
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