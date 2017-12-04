const cache = [];

const standartize = (arg) => {
    const defaults = {
        noCache: false,
        forceUpdate: false
    };

    if (arg instanceof String || typeof arg === 'string') {
        arg = {url: arg};
    }
    return Object.assign({}, defaults, arg)
};

export default function prefetch(arg) {
    arg = standartize(arg);
    if (arg.noCache) {
        return fetch(arg.url)
    }
    if (!cache.hasOwnProperty(arg.url) || arg.forceUpdate) {
        cache[arg.url] = fetch(arg.url)
    }
    return cache[arg.url]
}