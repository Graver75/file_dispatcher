/*
 *  Script exports React components from plugins
 */
const pluginsPathsObjectAwaited = require('./loader');

(async() => {
    let pluginsPathsObject = await pluginsPathsObjectAwaited;
    for (let pluginPathObject in pluginsPathsObject) {
        if (pluginsPathsObject.hasOwnProperty(pluginPathObject)) {
            let components = [];
            for (let componentPath of pluginsPathsObject[pluginPathObject]) {
                components.push(require(componentPath))
            }
            module.exports[pluginPathObject] = components
        }
    }
})();