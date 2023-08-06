/*! For license information please see chunk.6ba489447189c2c7127d.js.LICENSE.txt */
(self.webpackJsonp=self.webpackJsonp||[]).push([[58],{250:function(e,t,r){"use strict";r(249);var o=r(92),i=r(169),n=r(3);const a={getTabbableNodes:function(e){var t=[];return this._collectTabbableNodes(e,t)?i.a._sortByTabIndex(t):t},_collectTabbableNodes:function(e,t){if(e.nodeType!==Node.ELEMENT_NODE||!i.a._isVisible(e))return!1;var r,o=e,a=i.a._normalizedTabIndex(o),l=a>0;a>=0&&t.push(o),r="content"===o.localName||"slot"===o.localName?Object(n.a)(o).getDistributedNodes():Object(n.a)(o.shadowRoot||o.root||o).children;for(var s=0;s<r.length;s++)l=this._collectTabbableNodes(r[s],t)||l;return l}},l=customElements.get("paper-dialog"),s={get _focusableNodes(){return a.getTabbableNodes(this)}};class c extends(Object(o.b)([s],l)){}customElements.define("ha-paper-dialog",c)},859:function(e,t,r){"use strict";r.r(t),r.d(t,"HaDialogAisgalery",(function(){return m}));r(250),r(763);var o=r(80),i=r(0),n=r(57);function a(e){var t,r=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var o={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(o.decorators=e.decorators),"field"===e.kind&&(o.initializer=e.value),o}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function s(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var o=r.call(e,t||"default");if("object"!=typeof o)return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function u(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,o=new Array(t);r<t;r++)o[r]=e[r];return o}function f(e,t,r){return(f="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var o=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=h(e)););return e}(e,t);if(o){var i=Object.getOwnPropertyDescriptor(o,t);return i.get?i.get.call(r):i.value}})(e,t,r||e)}function h(e){return(h=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let m=function(e,t,r,o){var i=function(){(function(){return e});var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(o){t.forEach((function(t){var i=t.placement;if(t.kind===o&&("static"===i||"prototype"===i)){var n="static"===i?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var o=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===o?void 0:o.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],o=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!s(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),o.push.apply(o,t.finishers)}),this),!t)return{elements:r,finishers:o};var n=this.decorateConstructor(r,t);return o.push.apply(o,n.finishers),n.finishers=o,n},addElementPlacement:function(e,t,r){var o=t[e.placement];if(!r&&-1!==o.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");o.push(e.key)},decorateElement:function(e,t){for(var r=[],o=[],i=e.decorators,n=i.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var l=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,i[n])(l)||l);e=s.element,this.addElementPlacement(e,t),s.finisher&&o.push(s.finisher);var c=s.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:o,extras:r}},decorateConstructor:function(e,t){for(var r=[],o=t.length-1;o>=0;o--){var i=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[o])(i)||i);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var l=a+1;l<e.length;l++)if(e[a].key===e[l].key&&e[a].placement===e[l].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return u(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(r):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?u(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=p(e.key),o=String(e.placement);if("static"!==o&&"prototype"!==o&&"own"!==o)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+o+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:o,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var o=(0,t[r])(e);if(void 0!==o){if("function"!=typeof o)throw new TypeError("Finishers must return a constructor.");e=o}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(o)for(var n=0;n<o.length;n++)i=o[n](i);var f=t((function(e){i.initializeInstanceElements(e,h.elements)}),r),h=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},o=0;o<e.length;o++){var i,n=e[o];if("method"===n.kind&&(i=t.find(r)))if(c(n.descriptor)||c(i.descriptor)){if(s(n)||s(i))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");i.descriptor=n.descriptor}else{if(s(n)){if(s(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");i.decorators=n.decorators}l(n,i)}else t.push(n)}return t}(f.d.map(a)),e);return i.initializeClassElements(f.F,h.elements),i.runClassFinishers(f.F,h.finishers)}([Object(i.d)("ha-dialog-aisgalery")],(function(e,t){class r extends t{constructor(){super(),e(this),this.loadVaadin()}}return{F:r,d:[{kind:"get",static:!0,key:"styles",value:function(){return[n.c,i.c`
        :host {
          z-index: 103;
        }

        ha-icon-button {
          color: var(--secondary-text-color);
        }

        ha-icon-button[active] {
          color: var(--primary-color);
        }

        ha-paper-dialog {
          width: 450px;
          height: 350px;
        }
        a.button {
          text-decoration: none;
        }
        a.button > mwc-button {
          width: 100%;
        }
        .onboarding {
          padding: 0 24px;
        }
        paper-dialog-scrollable.top-border::before {
          content: "";
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 1px;
          background: var(--divider-color);
        }
      `]}},{kind:"field",decorators:[Object(i.h)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"_opened",value:()=>!1},{kind:"method",key:"showDialog",value:async function(){this._opened=!0,this.loadVaadin()}},{kind:"method",key:"render",value:function(){return i.f`
      <style>
        paper-dialog-scrollable {
          --paper-dialog-scrollable: {
            -webkit-overflow-scrolling: auto;
            max-height: 50vh !important;
          }
        }

        paper-dialog-scrollable.can-scroll {
          --paper-dialog-scrollable: {
            -webkit-overflow-scrolling: touch;
            max-height: 50vh !important;
          }
        }

        @media all and (max-width: 450px), all and (max-height: 500px) {
          paper-dialog-scrollable {
            --paper-dialog-scrollable: {
              -webkit-overflow-scrolling: auto;
              max-height: calc(100vh - 175px) !important;
            }
          }

          paper-dialog-scrollable.can-scroll {
            --paper-dialog-scrollable: {
              -webkit-overflow-scrolling: touch;
              max-height: calc(75vh - 175px) !important;
            }
          }
        }
        app-toolbar {
          margin: 0;
          padding: 0 16px;
          color: var(--primary-text-color);
          background-color: var(--secondary-background-color);
        }
        app-toolbar [main-title] {
          margin-left: 16px;
        }
      </style>
      <dom-module id="my-button" theme-for="vaadin-button">
        <template>
          <style>
            :host {
              color: var(--primary-color);
              border: 1px solid;
            }
          </style>
        </template>
      </dom-module>
      <ha-paper-dialog
        with-backdrop
        .opened=${this._opened}
        @opened-changed=${this._openedChanged}
      >
        <app-toolbar>
          <ha-icon-button icon="hass:close" dialog-dismiss=""></ha-icon-button>
          <div main-title="">Dodawanie zdjęć</div>
        </app-toolbar>
        <vaadin-upload
          capture="camera"
          accept="image/*"
          noAuto="false"
          style="text-align: center;"
        >
          <span slot="drop-label" style="color:white;"
            >Możesz przeciągnąć i upuścić tu.</span
          >
        </vaadin-upload>
      </ha-paper-dialog>
    `}},{kind:"method",key:"loadVaadin",value:async function(){customElements.whenDefined("vaadin-upload").then(async()=>{const e=this.shadowRoot.querySelector("vaadin-upload"),t=Object(o.c)();null!==e&&(e.set("i18n.addFiles.many","Wyślij zdjęcie [plik 5MB max] ..."),e.set("i18n.fileIsTooBig","Plik jest za duży. Maksymalnie można przesłać 5MB"),e.set("method","POST"),e.set("withCredentials",!0),e.set("target","api/ais_file/upload"),e.set("headers",{authorization:"Bearer "+t.access_token}),e.addEventListener("file-reject",(function(e){console.log(e.detail.file.name+" error: "+e.detail.error)})))})}},{kind:"method",key:"firstUpdated",value:function(e){f(h(r.prototype),"updated",this).call(this,e)}},{kind:"method",key:"updated",value:function(e){f(h(r.prototype),"updated",this).call(this,e)}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value,this.loadVaadin()}}]}}),i.a)}}]);
//# sourceMappingURL=chunk.6ba489447189c2c7127d.js.map