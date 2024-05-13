// CustomDirective.js

export default {
    mounted(el, binding) {
      const width = binding.value.width;
      const height = binding.value.height;
  
      if (width) {
        el.style.width = width;
      }
  
      if (height) {
        el.style.height = height;
      }
    }
  };
  