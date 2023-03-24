package com.virachlabo.temidialogflow.Interfaces;

import com.google.cloud.dialogflow.v2.DetectIntentResponse;

public interface DialogFlowAgentReponseCallback {

    public void DialogFlowAgentResponseListener(DetectIntentResponse detectIntentResponse);
}
