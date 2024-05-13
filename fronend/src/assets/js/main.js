const RegexPatterns = {
    email: /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    phone: /^\d{9,}$/
};

const inputValidation = (value, options = {}) => {
    const { required = true , minLen = null, maxLen = null, regex = null , lookalike = null} = options;
    // console.log(value)
    if(required === true && value.length === 0){
        return false;
    }

    if (minLen && value.length < minLen) {
        return false;
    }

    if (maxLen && value.length > maxLen) {
        return false;
    }

    if (regex  && !RegexPatterns[regex].test(value)) {
        return false;
    }

    if(lookalike && value !== lookalike ){
        return false;
    }

    return value;
};

export const inputsValidation  = (inputs,keysToExclude = []) => {
    const requestData = {}
    for (var i in inputs) {
        var input = inputs[i]
        var inputValue = inputValidation(input.value,input.validation)
        if(!inputValue){
            return false
        }
        requestData[i] = inputValue
      }
      const clenRequestData = excludeKeys(requestData, keysToExclude);
    return clenRequestData
}

function excludeKeys(obj, keysToExclude) {
    const result = {};
    for (const prop in obj) {
        if (obj.hasOwnProperty(prop) && !keysToExclude.includes(prop)) {
            result[prop] = obj[prop];
        }
    }
    return result;
}