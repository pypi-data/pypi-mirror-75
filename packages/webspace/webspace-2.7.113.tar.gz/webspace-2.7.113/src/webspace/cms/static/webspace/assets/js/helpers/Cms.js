import AccordionPure from './Accordion';

function createElementFromHTML(htmlString) {
  const div = document.createElement('div');
  div.innerHTML = htmlString.trim();
  return div.firstChild;
}

function animate(callbackObj, duration) {
  const requestAnimationFrame = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame;
  let startTime = 0;
  let percentage = 0;
  let
    animationTime = 0;

  duration = duration * 1000 || 1000;

  const animation = function ani(timestamp) {
    if (startTime === 0) {
      startTime = timestamp;
    } else {
      animationTime = timestamp - startTime;
    }

    if (typeof callbackObj.start === 'function' && startTime === timestamp) {
      callbackObj.start();

      requestAnimationFrame(animation);
    } else if (animationTime < duration) {
      if (typeof callbackObj.progress === 'function') {
        percentage = animationTime / duration;
        callbackObj.progress(percentage);
      }

      requestAnimationFrame(animation);
    } else if (typeof callbackObj.done === 'function') {
      callbackObj.done();
    }
  };
  return requestAnimationFrame(animation);
}

function easeInOutQuad(t) {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
}


const SmoothScroll = {
  init: () => {
    const offset = 50;
    const elements = document.querySelectorAll('a[href^="#"]');
    Array.prototype.forEach.call(elements, (el) => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const href = el.getAttribute('href');
        const elementHref = document.getElementById(href.replace('#', ''));
        const bodyRect = document.body.getBoundingClientRect();
        const elemRect = elementHref.getBoundingClientRect();
        const posY = elemRect.top - bodyRect.top;

        if (href !== '#') {
          window.scrollTo(0, posY - offset);
        }
      }, false);
    });
  },
};


const Carousel = {
  init: () => {
    const elements = document.getElementsByClassName('carousel');
    Array.prototype.forEach.call(elements, (el) => {
      const parent = el.parentNode;
      const theme = parent.getAttribute('class').split('theme-')[1];
      const right = createElementFromHTML(`<img class='s-icon x2 right' src='${Icons.right[theme]}' alt='Suivant'>`);
      const left = createElementFromHTML(`<img class='s-icon x2 left' src='${Icons.left[theme]}' alt='Précédent'>`);
      const scrollOffset = 305;
      parent.appendChild(right);
      parent.appendChild(left);
      let scroller = 0;
      right.addEventListener('click', (e) => {
        const sequenceObj = {};
        sequenceObj.progress = (function prog(percentage) {
          el.scrollLeft = scroller + easeInOutQuad(percentage) * scrollOffset;
        });
        animate(sequenceObj, 0.5);
        scroller = el.scrollLeft;
      });
      left.addEventListener('click', (e) => {
        const sequenceObj = {};
        sequenceObj.progress = (function prog(percentage) {
          el.scrollLeft = scroller - easeInOutQuad(percentage) * scrollOffset;
        });
        animate(sequenceObj, 0.5);
        scroller = el.scrollLeft;
      });
    });
  },
};

const Clicker = {
  init: () => {
    document.addEventListener('click', (e) => {
      const elements = document.querySelectorAll('*[data-clicker-child]');
      Array.prototype.forEach.call(elements, (el) => {
        el.style.display = 'none';
      });
    });

    const elements = document.querySelectorAll('*[data-clicker]');
    Array.prototype.forEach.call(elements, (el) => {
      el.addEventListener('click', (e) => {
        e.stopPropagation();
        const child = el.querySelectorAll('*[data-clicker-child]')[0];
        const childIsVisible = child.style.visibility !== 'hidden';
        const all = document.querySelectorAll('*[data-clicker-child]');

        Array.prototype.forEach.call(all, (ell) => {
          ell.style.display = 'none';
        });
        if (childIsVisible) child.style.display = 'block';
      });
    });
  },
};

const Aside = {
  mobile: () => {
    const accordion = document.getElementById('aside-mobile');
    const accordionOpen = document.getElementById('aside-mobile-open');
    const accordionClose = document.getElementById('aside-mobile-close');

    if (accordion) {
      document.addEventListener('click', (e) => {
        accordion.style.right = '-100%';
      });

      accordionOpen.addEventListener('click', (e) => {
        e.stopPropagation();
        accordion.style.right = '0';
      });

      accordionClose.addEventListener('click', (e) => {
        e.stopPropagation();
        accordion.style.right = '-100%';
      });
    }
  },
};

const Lazy = {
  init: () => {
    const io = new IntersectionObserver(entries => entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const element = entry.target;
        if (element.id.startsWith('block')) {
          // background
          element.style.backgroundImage = `url(${element.dataset.src})`;
        } else {
          // classic
          element.src = element.dataset.src;
        }
        io.unobserve(element);
      }
    }));
    document.querySelectorAll('.lazy').forEach(element => io.observe(element));
  },
};


const Collect = {
  init: () => {
    const collectBlock = document.getElementById('collect-block');
    const collectButton = document.getElementById('collect-btn');
    const haveAccepted = localStorage.getItem('collect');

    if (!(haveAccepted && haveAccepted === 'false')) {
      collectBlock.children[0].style.display = 'flex';
      collectButton.addEventListener('click', (e) => {
        e.stopPropagation();
        collectBlock.style.display = 'none';
        localStorage.setItem('collect', 'false');
      });
    } else {
      collectBlock.style.display = 'none';
    }
  },
};


const Accordion = {
  init: () => {
    const accordions = Array.from(document.querySelectorAll('.accordion-container'));
    if (accordions) {
      accordions.forEach((item) => {
        new AccordionPure(`#${item.id}`, {
          duration: 300,
        });
      });
    }
  },
};

const CounterUp = {
  init: () => {
    const io = new IntersectionObserver(entries => entries.forEach((item) => {
      const element = item.target;
      if (item.isIntersecting) {
        const number = Number(element.textContent) + 1;

        let counter = 0;
        function counterJs() {
          element.innerHTML = counter.toString();
          counter += 1;
          if (counter < number) {
            setTimeout(() => {
              counterJs();
            }, 50);
          }
        }

        counterJs();
        io.unobserve(element);
      }
    }));
    document.querySelectorAll('.counter-up').forEach(element => io.observe(element));
  },
};

const Animation = {
  init: () => {
    const io = new IntersectionObserver(entries => entries.forEach((item) => {
      const element = item.target;
      if (item.isIntersecting) {
        element.classList.add('start');
        io.unobserve(element);
      }
    }));
    document.querySelectorAll('.animation').forEach(element => io.observe(element));
  },
};

export default {
  Image,
  Carousel,
  SmoothScroll,
  Clicker,
  Aside,
  Lazy,
  Collect,
  Accordion,
  CounterUp,
  Animation,
};
