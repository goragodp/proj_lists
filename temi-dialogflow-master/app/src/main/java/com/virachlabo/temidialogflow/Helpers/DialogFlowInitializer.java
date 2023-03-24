package com.virachlabo.temidialogflow.Helpers;

import android.content.Context;
import android.util.Log;

import com.google.api.client.util.Lists;
import com.google.api.gax.core.FixedCredentialsProvider;
import com.google.auth.oauth2.GoogleCredentials;
import com.google.auth.oauth2.ServiceAccountCredentials;
import com.google.cloud.dialogflow.v2.SessionName;
import com.google.cloud.dialogflow.v2.SessionsClient;

import java.io.InputStream;
import java.util.Collection;
import java.util.Collections;
import java.util.UUID;

import com.google.cloud.dialogflow.v2.SessionsSettings;
import com.virachlabo.temidialogflow.R;

public class DialogFlowInitializer {
    private SessionsClient sessionsClient;
    private SessionName sessionName;
    private String uuid = UUID.randomUUID().toString();
    private String TAG = "DialogFlowInitializer";
    private String projectID;

    public DialogFlowInitializer(Context context) {
        try {
            //Read json credential file
            InputStream stream = context.getResources().openRawResource(R.raw.credential);
            //Create Google credential login
            GoogleCredentials credentials = GoogleCredentials.fromStream(stream)
                    .createScoped(Lists.newArrayList(Collections.singleton("https://www.googleapis.com/auth/cloud-platform")));
            //get project ID from credential
            this.projectID = ((ServiceAccountCredentials) credentials).getProjectId();
            //Create Session
            SessionsSettings.Builder settingBuilder = SessionsSettings.newBuilder();
            SessionsSettings sessionsSettings = settingBuilder.setCredentialsProvider(
                    FixedCredentialsProvider.create(credentials)
            ).build();
            //use sessionSetting to create client
            this.sessionsClient = SessionsClient.create(sessionsSettings);
            this.sessionName = SessionName.of(this.projectID, this.uuid);

            Log.i(TAG, "DialogflowInitializer: Successfully create session from json");

        }catch (Exception e) {
            Log.e(TAG, "DialogFlowInitializer:" + e.getMessage());

        }
    }

    public SessionName getSessionName() {return sessionName;}
    public SessionsClient getSessionsClient() {return sessionsClient;}
    public String getProjectID() {return projectID;}
}
