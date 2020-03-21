export function toArrowFuncString(func) {
    // Takes any function and formats it as a arrow function expression, like `() => { ... }`
    // It is necessary to use this function to reformat all function that function as listeners
    // in `on` method calls for d3 objects. Reason: d3 invokes the listener within the `this`
    // context of the simulation, and class methods are in the class context so cannot  be passed.
    return '() => {' + func.toString().split('\n').splice(1).join('\n');
}

export function valIfValid(v, alt) {
    // Use this instead of (v || alt) which won't work when v is 0
    if (typeof(v) == "number") return v;
    if (typeof(v) == "string") return v;
    return alt;
}

export class DefaultDict {
    constructor(defaultInit) {
        return new Proxy({}, {
            get: (target, name) => name in target ?
                target[name] :
                (target[name] = typeof defaultInit === 'function' ?
                    new defaultInit().valueOf() :
                    defaultInit)
        })
    }
}