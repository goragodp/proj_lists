package com.virachlabo.temidialogflow.Helpers;

import android.os.AsyncTask;
import android.util.Log;

import com.google.cloud.dialogflow.v2.DetectIntentRequest;
import com.google.cloud.dialogflow.v2.DetectIntentResponse;
import com.google.cloud.dialogflow.v2.QueryInput;
import com.google.cloud.dialogflow.v2.SessionName;
import com.google.cloud.dialogflow.v2.SessionsClient;
import com.virachlabo.temidialogflow.Interfaces.DialogFlowAgentReponseCallback;

public class DialogFlowAgentRequest extends AsyncTask<Void, Void, DetectIntentResponse> {

    private SessionName session;
    private SessionsClient sessionsClient;
    private QueryInput queryInput;
    private String TAG = "DialogFlowAgentRequest";
    private DialogFlowAgentReponseCallback agentReponseCallback;

    public DialogFlowAgentRequest(DialogFlowAgentReponseCallback agentResponse,
                                   SessionName sessionsName, SessionsClient sessionsClient, QueryInput queryInput) {
        this.session = sessionsName;
        this.sessionsClient = sessionsClient;
        this.queryInput = queryInput;
        this.agentReponseCallback = agentResponse;
    }

    @Override
    protected DetectIntentResponse doInBackground(Void... voids) {
        try {
            DetectIntentRequest detectIntentRequest = DetectIntentRequest.newBuilder()
                    .setSession(session.toString())
                    .setQueryInput(queryInput)
                    .build();
            return sessionsClient.detectIntent(detectIntentRequest);
        }catch (Exception e) {
            Log.i(TAG, "DoInBg:" + e.getMessage());
        }
        return null;
    }

    @Override
    protected void onPostExecute(DetectIntentResponse detectIntentResponse) {
        Log.i(TAG, "onPostExecution");
        agentReponseCallback.DialogFlowAgentResponseListener(detectIntentResponse);
    }
}
