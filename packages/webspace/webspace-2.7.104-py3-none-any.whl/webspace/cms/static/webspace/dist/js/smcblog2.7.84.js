!function(e){var t={};function n(o){if(t[o])return t[o].exports;var r=t[o]={i:o,l:!1,exports:{}};return e[o].call(r.exports,r,r.exports,n),r.l=!0,r.exports}n.m=e,n.c=t,n.d=function(e,t,o){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:o})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var o=Object.create(null);if(n.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)n.d(o,r,function(t){return e[t]}.bind(null,r));return o},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="/",n(n.s=6)}({6:function(e,t,n){"use strict";function o(e,t){const n=t.getBoundingClientRect().top-document.body.getBoundingClientRect().top,o=t.getBoundingClientRect().bottom-document.body.getBoundingClientRect().top-window.innerHeight;document.documentElement.scrollTop>o?(e.style.position="absolute",e.style.top="unset",e.style.bottom="0px"):document.documentElement.scrollTop>n?(e.style.position="fixed",e.style.top="0px",e.style.bottom="unset"):(e.style.position="absolute",e.style.top="unset",e.style.bottom="unset")}n.r(t);var r={summary:()=>{const e=document.getElementById("blog-content-container"),t=document.getElementById("block-summary");o(t,e),window.addEventListener("scroll",()=>{o(t,e)})},summaryTitles:()=>{const e=document.getElementById("block-summary"),t=new IntersectionObserver(t=>t.forEach(t=>{const n=t.target;if(t.isIntersecting){e.querySelectorAll('a[class^="active"]').forEach(e=>e.classList.remove("active"));e.querySelector(`a[href="#${n.id}"]`).classList.add("active")}}));document.querySelectorAll('h2[id^="titles"]').forEach(e=>t.observe(e))}};r.summary(),r.summaryTitles()}});