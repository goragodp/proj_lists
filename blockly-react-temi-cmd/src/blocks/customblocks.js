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
 * @fileoverview Define custom blocks.
 * @author samelh@google.com (Sam El-Husseini)
 */

// More on defining blocks:
// https://developers.google.com/blockly/guides/create-custom-blocks/define-blocks

import * as Blockly from 'blockly/core';

// Since we're using json to initialize the field, we'll need to import it.
import '../fields/BlocklyReactField';
import '../fields/DateField';
import { Block } from '../Blockly';
//Temi block
Blockly.Blocks['speech_say'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Say")
        .appendField(new Blockly.FieldTextInput("hello world"), "utterance")
        .appendField("in")
        .appendField(new Blockly.FieldDropdown([["Thai","th"], ["English","en"], ["Japanese","JP"]]), "language_options");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(315);
 this.setTooltip("Type what you want temi to say, select languge either English, Japanese or Thai");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['call_person'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Call")
        .appendField(new Blockly.FieldDropdown([["Man","fe1090ed941db12ed1d350730031ea5b"], ["Pear","4990c18cea5e6604cc1adc384fe224e8"], ["AjVirach","67696f1ff709a3b0804ae43641ed8d85"]]), "contact");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("Select person to call");
  }
};

Blockly.Blocks['event_block'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Event:")
        .appendField(new Blockly.FieldDropdown([["out of bed","EVT_OUT_OF_BED"], ["sitting","EVT_SIT_ON_BED"]]), "event");
    this.appendStatementInput("event_out_of_bed")
        .setCheck(null);
    this.setColour(230);
 this.setTooltip("event for block (none-sequence)");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['locations_goto'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Go to")
        .appendField(new Blockly.FieldTextInput("kitchen"), "location");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("Command temi to go to a pre-defined location");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['temi_start'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Start Temi blockly programming")
        .appendField(new Blockly.FieldTextInput(""), "TEMI_SERIAL");
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("Enter the serial number on Temi Screen");
 this.setHelpUrl("");
  }
};

// UNDERDEVELOP -------------------------------------------

Blockly.Blocks['follow_unconstrained'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Follow");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(180);
 this.setTooltip("Follow the nearest person in front of temi");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['follow_constrained'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Follow")
        .appendField("(in-place)");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(180);
 this.setTooltip("Follow (in-place) the nearest person in front of temi");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['movement_turn'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Turn")
        .appendField(new Blockly.FieldAngle(90), "angle");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(0);
 this.setTooltip("Turn temi by a specified angle");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['movement_tilt'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Tilt")
        .appendField(new Blockly.FieldNumber(0, -15, 55), "angle");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(0);
 this.setTooltip("Tilt temi by a specified angle. Choose a value between -15 and 55.");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['movement_joystick'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Move")
        .appendField("X:")
        .appendField(new Blockly.FieldNumber(0), "x")
        .appendField("Y:")
        .appendField(new Blockly.FieldNumber(0), "y");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(0);
 this.setTooltip("Move temi along the X and Y axis");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['movement'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Moves")
        .appendField(new Blockly.FieldDropdown([["forward","FWD"], ["baackward","BWD"]]), "direction");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("define direction of movement");
 this.setHelpUrl("");
  }
};

Blockly.Blocks['locations_go_home'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Return Home");
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("Command temi to return Home");
 this.setHelpUrl("");
  }
};

// Blockly.Blocks['call_person'] = {
//   init: function() {
//     this.appendDummyInput()
//         .appendField("Call")
//         .appendField(new Blockly.FieldTextInput(""), "contact");
//     this.setPreviousStatement(true, null);
//     this.setNextStatement(true, null);
//     this.setColour(230);
//  this.setTooltip("Call a person in contact list");
//  this.setHelpUrl("");
//   }
// };
