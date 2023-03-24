/**
 * @license
 *
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @fileoverview Define generation methods for custom blocks.
 * @author samelh@google.com (Sam El-Husseini)
 */

// More on generating code:
// https://developers.google.com/blockly/guides/create-custom-blocks/generating-code

import * as Blockly from 'blockly/core';
import 'blockly/javascript';
import 'blockly/python';

Blockly.JavaScript['test_react_field'] = function (block) {
  return "console.log('custom block');\n";
};

Blockly.JavaScript['test_react_date_field'] = function (block) {
  return 'console.log(' + block.getField('DATE').getText() + ');\n';
};

//temi customn block
Blockly.Python['speech_say'] = function(block) {
  var text_utterance = block.getFieldValue('utterance');
  var dropdown_language_options = block.getFieldValue("language_options");
  // var code = `robot.speak(TtsRequest.create("${text_utterance}", false));\n`;
  var code = `robot.speak("${text_utterance}", "${dropdown_language_options}")\n`
  return code;
};

Blockly.Python['locations_goto'] = function(block) {
  var text_location = block.getFieldValue('location');
  // var code = `robot.goTo("${text_location}");\n`; 
  // var code = `actionlist.append('{"action":"GOTO", "content":"${text_location}"}')\n`
  var code = `robot.goto("${text_location}")\n`
  // @TODO Add wait
  return code;
};


Blockly.Python['call_person'] = function(block) {
  var dropdown_contact = block.getFieldValue('contact');
  // var code = `actionlist.append('{"action":"CALL", "content":"${dropdown_contact}"}')\n`
  var code = `robot.call("${dropdown_contact}")\n`
  return code;
};

Blockly.Python['locations_go_home'] = function(block) {
  // var code = `actionlist.append('{"action":"GOTO", "content":"Home Base"}')\n`
  var code = `robot.goto('home base')\n`
  return code;
};

Blockly.Python['temi_start'] = function(block) {
  var text_temi_serial = block.getFieldValue('TEMI_SERIAL');
  Blockly.Python.provideFunction_('temi_start_import', ['import robot as temi', 
                        'from interface import CommandInterface', 
                        `temi_serial = "${text_temi_serial}"`,
                        'mqtt = CommandInterface()',
                        'mqtt.connect()',
                        'robot = temi.Robot(mqtt, temi_serial)'
  ])
  var code = '#--------- The program start here -----------\n';
  return code;
};

// UNDERDEVELOP----------------------------------------------------------
Blockly.Python['movement'] = function(block) {
  var dropdown_direction = block.getFieldValue('direction');
  var code = `robot.move(${dropdown_direction})\n`;
  return code;
}

Blockly.Python['follow_unconstrained'] = function(block) {
  var code = `robot.beWithMe();\n`;
  return code;
};

Blockly.Python['follow_constrained'] = function(block) {
  var code = `robot.constraintBeWith();\n`;
  return code;
};

Blockly.Python['movement_turn'] = function(block) {
  var number_angle = block.getFieldValue('angle');
  var code = `robot.turnBy(${number_angle});\n`;
  return code;
};

Blockly.Python['movement_tilt'] = function(block) {
  var number_angle = block.getFieldValue('angle');
  var code = `robot.tiltBy(${number_angle});\n`;
  return code;
};

Blockly.Python['movement_joystick'] = function(block) {
  var number_x = block.getFieldValue('x');
  var number_y = block.getFieldValue('y');
  var code = `robot.skidJoy(${number_x}, ${number_y});\n`;
  return code;
};



Blockly.Python['event_block'] = function(block) {
  var dropdown_event = block.getFieldValue('event');
  var statements_event_out_of_bed = Blockly.JavaScript.statementToCode(block, 'event_out_of_bed');
  // TODO: Assemble JavaScript into code variable.
  var code = '...;\n';
  return code;
};