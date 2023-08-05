// Copyright (c) wangsijie
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import React from 'react';
import ReactDOM from 'react-dom';
import Quiz from '@boyuai/quiz';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

// Import the CSS
import '../css/widget.css'


export
class QuizModel extends DOMWidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: QuizModel.model_name,
      _model_module: QuizModel.model_module,
      _model_module_version: QuizModel.model_module_version,
      _view_name: QuizModel.view_name,
      _view_module: QuizModel.view_module,
      _view_module_version: QuizModel.view_module_version,
      value: [],
      quizId: '',
    };
  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
      // Add any extra serializers here
    }

  static model_name = 'QuizModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'QuizView';   // Set to null if no view
  static view_module = MODULE_NAME;   // Set to null if no view
  static view_module_version = MODULE_VERSION;
}


export
class QuizView extends DOMWidgetView {
  render() {
    if (!document.getElementById('katex-css')) {
      const link = document.createElement('link');
      link.id = 'katex-css';
      link.rel = 'stylesheet';
      link.href = 'https://cdn.jsdelivr.net/npm/katex/dist/katex.min.css';
      document.head.appendChild(link);
    }

    this.el.htmlContent = '';
    this.initReact();
  }

  initReact() {
    const value = this.model.get('value');
    const id = this.model.get('quiz_id');
    if (!id) {
      this.el.textContent = 'quizId必须指定';
      return;
    }
    const userValue = window[`__ipyquiz_${id}_value`];
    const _handleSubmit = window[`__ipyquiz_${id}_submit`];
    const handleSubmit = (answers, rightCount) => {
      if (typeof _handleSubmit === 'function') {
        _handleSubmit(answers, rightCount, value);
      }
    }
    ReactDOM.render(
      <div>
        <Quiz questions={value} values={userValue} onSubmit={handleSubmit} />
      </div>,
      this.el,
    );
  }
}
