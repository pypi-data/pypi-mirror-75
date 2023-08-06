/*! For license information please see chunk.bd9dad6f40bf3114cd49.js.LICENSE.txt */
(self.webpackJsonp=self.webpackJsonp||[]).push([[172],{164:function(e,t,a){"use strict";a(5);var r=a(70),o=a(71);const i={properties:{checked:{type:Boolean,value:!1,reflectToAttribute:!0,notify:!0,observer:"_checkedChanged"},toggles:{type:Boolean,value:!0,reflectToAttribute:!0},value:{type:String,value:"on",observer:"_valueChanged"}},observers:["_requiredChanged(required)"],created:function(){this._hasIronCheckedElementBehavior=!0},_getValidity:function(e){return this.disabled||!this.required||this.checked},_requiredChanged:function(){this.required?this.setAttribute("aria-required","true"):this.removeAttribute("aria-required")},_checkedChanged:function(){this.active=this.checked,this.fire("iron-change")},_valueChanged:function(){void 0!==this.value&&null!==this.value||(this.value="on")}},c=[r.a,o.a,i];var n=a(103),l=a(124);a.d(t,"a",(function(){return p}));const s={_checkedChanged:function(){i._checkedChanged.call(this),this.hasRipple()&&(this.checked?this._ripple.setAttribute("checked",""):this._ripple.removeAttribute("checked"))},_buttonStateChanged:function(){l.a._buttonStateChanged.call(this),this.disabled||this.isAttached&&(this.checked=this.active)}},p=[n.a,c,s]},166:function(e,t,a){"use strict";a(5),a(52);var r=a(164),o=a(103),i=a(6),c=a(4),n=a(72);const l=c.a`<style>
  :host {
    display: inline-block;
    white-space: nowrap;
    cursor: pointer;
    --calculated-paper-checkbox-size: var(--paper-checkbox-size, 18px);
    /* -1px is a sentinel for the default and is replaced in \`attached\`. */
    --calculated-paper-checkbox-ink-size: var(--paper-checkbox-ink-size, -1px);
    @apply --paper-font-common-base;
    line-height: 0;
    -webkit-tap-highlight-color: transparent;
  }

  :host([hidden]) {
    display: none !important;
  }

  :host(:focus) {
    outline: none;
  }

  .hidden {
    display: none;
  }

  #checkboxContainer {
    display: inline-block;
    position: relative;
    width: var(--calculated-paper-checkbox-size);
    height: var(--calculated-paper-checkbox-size);
    min-width: var(--calculated-paper-checkbox-size);
    margin: var(--paper-checkbox-margin, initial);
    vertical-align: var(--paper-checkbox-vertical-align, middle);
    background-color: var(--paper-checkbox-unchecked-background-color, transparent);
  }

  #ink {
    position: absolute;

    /* Center the ripple in the checkbox by negative offsetting it by
     * (inkWidth - rippleWidth) / 2 */
    top: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    left: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    width: var(--calculated-paper-checkbox-ink-size);
    height: var(--calculated-paper-checkbox-ink-size);
    color: var(--paper-checkbox-unchecked-ink-color, var(--primary-text-color));
    opacity: 0.6;
    pointer-events: none;
  }

  #ink:dir(rtl) {
    right: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    left: auto;
  }

  #ink[checked] {
    color: var(--paper-checkbox-checked-ink-color, var(--primary-color));
  }

  #checkbox {
    position: relative;
    box-sizing: border-box;
    height: 100%;
    border: solid 2px;
    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
    border-radius: 2px;
    pointer-events: none;
    -webkit-transition: background-color 140ms, border-color 140ms;
    transition: background-color 140ms, border-color 140ms;

    -webkit-transition-duration: var(--paper-checkbox-animation-duration, 140ms);
    transition-duration: var(--paper-checkbox-animation-duration, 140ms);
  }

  /* checkbox checked animations */
  #checkbox.checked #checkmark {
    -webkit-animation: checkmark-expand 140ms ease-out forwards;
    animation: checkmark-expand 140ms ease-out forwards;

    -webkit-animation-duration: var(--paper-checkbox-animation-duration, 140ms);
    animation-duration: var(--paper-checkbox-animation-duration, 140ms);
  }

  @-webkit-keyframes checkmark-expand {
    0% {
      -webkit-transform: scale(0, 0) rotate(45deg);
    }
    100% {
      -webkit-transform: scale(1, 1) rotate(45deg);
    }
  }

  @keyframes checkmark-expand {
    0% {
      transform: scale(0, 0) rotate(45deg);
    }
    100% {
      transform: scale(1, 1) rotate(45deg);
    }
  }

  #checkbox.checked {
    background-color: var(--paper-checkbox-checked-color, var(--primary-color));
    border-color: var(--paper-checkbox-checked-color, var(--primary-color));
  }

  #checkmark {
    position: absolute;
    width: 36%;
    height: 70%;
    border-style: solid;
    border-top: none;
    border-left: none;
    border-right-width: calc(2/15 * var(--calculated-paper-checkbox-size));
    border-bottom-width: calc(2/15 * var(--calculated-paper-checkbox-size));
    border-color: var(--paper-checkbox-checkmark-color, white);
    -webkit-transform-origin: 97% 86%;
    transform-origin: 97% 86%;
    box-sizing: content-box; /* protect against page-level box-sizing */
  }

  #checkmark:dir(rtl) {
    -webkit-transform-origin: 50% 14%;
    transform-origin: 50% 14%;
  }

  /* label */
  #checkboxLabel {
    position: relative;
    display: inline-block;
    vertical-align: middle;
    padding-left: var(--paper-checkbox-label-spacing, 8px);
    white-space: normal;
    line-height: normal;
    color: var(--paper-checkbox-label-color, var(--primary-text-color));
    @apply --paper-checkbox-label;
  }

  :host([checked]) #checkboxLabel {
    color: var(--paper-checkbox-label-checked-color, var(--paper-checkbox-label-color, var(--primary-text-color)));
    @apply --paper-checkbox-label-checked;
  }

  #checkboxLabel:dir(rtl) {
    padding-right: var(--paper-checkbox-label-spacing, 8px);
    padding-left: 0;
  }

  #checkboxLabel[hidden] {
    display: none;
  }

  /* disabled state */

  :host([disabled]) #checkbox {
    opacity: 0.5;
    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
  }

  :host([disabled][checked]) #checkbox {
    background-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
    opacity: 0.5;
  }

  :host([disabled]) #checkboxLabel  {
    opacity: 0.65;
  }

  /* invalid state */
  #checkbox.invalid:not(.checked) {
    border-color: var(--paper-checkbox-error-color, var(--error-color));
  }
</style>

<div id="checkboxContainer">
  <div id="checkbox" class$="[[_computeCheckboxClass(checked, invalid)]]">
    <div id="checkmark" class$="[[_computeCheckmarkClass(checked)]]"></div>
  </div>
</div>

<div id="checkboxLabel"><slot></slot></div>`;l.setAttribute("strip-whitespace",""),Object(i.a)({_template:l,is:"paper-checkbox",behaviors:[r.a],hostAttributes:{role:"checkbox","aria-checked":!1,tabindex:0},properties:{ariaActiveAttribute:{type:String,value:"aria-checked"}},attached:function(){Object(n.a)(this,(function(){if("-1px"===this.getComputedStyleValue("--calculated-paper-checkbox-ink-size").trim()){var e=this.getComputedStyleValue("--calculated-paper-checkbox-size").trim(),t="px",a=e.match(/[A-Za-z]+$/);null!==a&&(t=a[0]);var r=parseFloat(e),o=8/3*r;"px"===t&&(o=Math.floor(o))%2!=r%2&&o++,this.updateStyles({"--paper-checkbox-ink-size":o+t})}}))},_computeCheckboxClass:function(e,t){var a="";return e&&(a+="checked "),t&&(a+="invalid"),a},_computeCheckmarkClass:function(e){return e?"":"hidden"},_createRipple:function(){return this._rippleContainer=this.$.checkboxContainer,o.b._createRipple.call(this)}})},167:function(e,t,a){"use strict";a.d(t,"a",(function(){return p}));const r=Symbol("Comlink.proxy"),o=Symbol("Comlink.endpoint"),i=Symbol("Comlink.releaseProxy"),c=Symbol("Comlink.thrown"),n=e=>"object"==typeof e&&null!==e||"function"==typeof e,l=new Map([["proxy",{canHandle:e=>n(e)&&e[r],serialize(e){const{port1:t,port2:a}=new MessageChannel;return function e(t,a=self){a.addEventListener("message",(function o(i){if(!i||!i.data)return;const{id:n,type:l,path:p}=Object.assign({path:[]},i.data),h=(i.data.argumentList||[]).map(k);let d;try{const a=p.slice(0,-1).reduce((e,t)=>e[t],t),o=p.reduce((e,t)=>e[t],t);switch(l){case 0:d=o;break;case 1:a[p.slice(-1)[0]]=k(i.data.value),d=!0;break;case 2:d=o.apply(a,h);break;case 3:d=function(e){return Object.assign(e,{[r]:!0})}(new o(...h));break;case 4:{const{port1:a,port2:r}=new MessageChannel;e(t,r),d=function(e,t){return u.set(e,t),e}(a,[a])}break;case 5:d=void 0}}catch(m){d={value:m,[c]:0}}Promise.resolve(d).catch(e=>({value:e,[c]:0})).then(e=>{const[t,r]=b(e);a.postMessage(Object.assign(Object.assign({},t),{id:n}),r),5===l&&(a.removeEventListener("message",o),s(a))})})),a.start&&a.start()}(e,t),[a,[a]]},deserialize:e=>(e.start(),p(e))}],["throw",{canHandle:e=>n(e)&&c in e,serialize({value:e}){let t;return t=e instanceof Error?{isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:{isError:!1,value:e},[t,[]]},deserialize(e){if(e.isError)throw Object.assign(new Error(e.value.message),e.value);throw e.value}}]]);function s(e){(function(e){return"MessagePort"===e.constructor.name})(e)&&e.close()}function p(e,t){return function e(t,a=[],r=function(){}){let c=!1;const n=new Proxy(r,{get(r,o){if(h(c),o===i)return()=>m(t,{type:5,path:a.map(e=>e.toString())}).then(()=>{s(t),c=!0});if("then"===o){if(0===a.length)return{then:()=>n};const e=m(t,{type:0,path:a.map(e=>e.toString())}).then(k);return e.then.bind(e)}return e(t,[...a,o])},set(e,r,o){h(c);const[i,n]=b(o);return m(t,{type:1,path:[...a,r].map(e=>e.toString()),value:i},n).then(k)},apply(r,i,n){h(c);const l=a[a.length-1];if(l===o)return m(t,{type:4}).then(k);if("bind"===l)return e(t,a.slice(0,-1));const[s,p]=d(n);return m(t,{type:2,path:a.map(e=>e.toString()),argumentList:s},p).then(k)},construct(e,r){h(c);const[o,i]=d(r);return m(t,{type:3,path:a.map(e=>e.toString()),argumentList:o},i).then(k)}});return n}(e,[],t)}function h(e){if(e)throw new Error("Proxy has been released and is not useable")}function d(e){const t=e.map(b);return[t.map(e=>e[0]),(a=t.map(e=>e[1]),Array.prototype.concat.apply([],a))];var a}const u=new WeakMap;function b(e){for(const[t,a]of l)if(a.canHandle(e)){const[r,o]=a.serialize(e);return[{type:3,name:t,value:r},o]}return[{type:0,value:e},u.get(e)||[]]}function k(e){switch(e.type){case 3:return l.get(e.name).deserialize(e.value);case 0:return e.value}}function m(e,t,a){return new Promise(r=>{const o=new Array(4).fill(0).map(()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16)).join("-");e.addEventListener("message",(function t(a){a.data&&a.data.id&&a.data.id===o&&(e.removeEventListener("message",t),r(a.data))})),e.start&&e.start(),e.postMessage(Object.assign({id:o},t),a)})}},186:function(e,t,a){"use strict";a(5),a(47),a(55),a(142);var r=a(6),o=a(4),i=a(102);Object(r.a)({_template:o.a`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[i.a]})},278:function(e,t,a){"use strict";a(5),a(47),a(52);var r=a(232),o=a(6),i=a(4);Object(o.a)({_template:i.a`
    <style>

      :host {
        display: block;
        @apply --layout-relative;
      }

      :host(.is-scrolled:not(:first-child))::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      :host(.can-scroll:not(.scrolled-to-bottom):not(:last-child))::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      .scrollable {
        padding: 0 24px;

        @apply --layout-scroll;
        @apply --paper-dialog-scrollable;
      }

      .fit {
        @apply --layout-fit;
      }
    </style>

    <div id="scrollable" class="scrollable" on-scroll="updateScrollState">
      <slot></slot>
    </div>
`,is:"paper-dialog-scrollable",properties:{dialogElement:{type:Object}},get scrollTarget(){return this.$.scrollable},ready:function(){this._ensureTarget(),this.classList.add("no-padding")},attached:function(){this._ensureTarget(),requestAnimationFrame(this.updateScrollState.bind(this))},updateScrollState:function(){this.toggleClass("is-scrolled",this.scrollTarget.scrollTop>0),this.toggleClass("can-scroll",this.scrollTarget.offsetHeight<this.scrollTarget.scrollHeight),this.toggleClass("scrolled-to-bottom",this.scrollTarget.scrollTop+this.scrollTarget.offsetHeight>=this.scrollTarget.scrollHeight)},_ensureTarget:function(){this.dialogElement=this.dialogElement||this.parentElement,this.dialogElement&&this.dialogElement.behaviors&&this.dialogElement.behaviors.indexOf(r.b)>=0?(this.dialogElement.sizingTarget=this.scrollTarget,this.scrollTarget.classList.remove("fit")):this.dialogElement&&this.scrollTarget.classList.add("fit")}})}}]);
//# sourceMappingURL=chunk.bd9dad6f40bf3114cd49.js.map