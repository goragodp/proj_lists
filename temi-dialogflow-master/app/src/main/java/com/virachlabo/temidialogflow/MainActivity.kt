package com.virachlabo.temidialogflow

import android.content.pm.PackageManager
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import com.google.cloud.dialogflow.v2.DetectIntentResponse
import com.google.cloud.dialogflow.v2.QueryInput
import com.google.cloud.dialogflow.v2.TextInput
import com.robotemi.sdk.Robot
import com.robotemi.sdk.TtsRequest
import com.robotemi.sdk.exception.OnSdkExceptionListener
import com.robotemi.sdk.exception.SdkException
import com.robotemi.sdk.listeners.OnRobotReadyListener
import com.virachlabo.temidialogflow.Helpers.DialogFlowAgentRequest
import com.virachlabo.temidialogflow.Helpers.DialogFlowInitializer
import com.virachlabo.temidialogflow.Interfaces.DialogFlowAgentReponseCallback
import java.lang.RuntimeException

class MainActivity : AppCompatActivity(), OnRobotReadyListener, Robot.TtsListener,
OnSdkExceptionListener, Robot.WakeupWordListener, DialogFlowAgentReponseCallback{

    private lateinit var robot: Robot
    private var TAG: String = "Main Robot Activity"
    private lateinit var dialogFlowInitializer: DialogFlowInitializer;


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        robot = Robot.getInstance()
        dialogFlowInitializer = DialogFlowInitializer(this);
    }

    private fun speak(msg: String) {
        val ttsRequest: TtsRequest = TtsRequest.create(msg, language = TtsRequest.Language.EN_US)
        robot.speak(ttsRequest)
    }

    private fun sendMessageToAgent(msg: String) {
        val input:QueryInput = QueryInput.newBuilder()
            .setText(TextInput.newBuilder().setText(msg).setLanguageCode("en-US"))
            .build()

        DialogFlowAgentRequest(this,
        dialogFlowInitializer.sessionName,
        dialogFlowInitializer.sessionsClient,
        input).execute()
    }
    override fun onStart() {
        super.onStart()
        robot.addOnRobotReadyListener(this)
        robot.addTtsListener(this)
        robot.addOnSdkExceptionListener(this)
        robot.addWakeupWordListener(this)
    }

    override fun onStop() {
        robot.removeWakeupWordListener(this)
        robot.removeOnSdkExceptionListener(this)
        robot.removeOnRobotReadyListener(this)
        robot.removeTtsListener(this)
        super.onStop()
    }

    override fun onRobotReady(isReady: Boolean) {
        if(isReady) {
            try {
                val activityInfo = packageManager.getActivityInfo(componentName, PackageManager.GET_META_DATA)
                robot.onStart(activityInfo)
                sendMessageToAgent("Hey")

            }catch (e: PackageManager.NameNotFoundException) {
                throw RuntimeException(e)
            }
        }
    }

    override fun onTtsStatusChanged(ttsRequest: TtsRequest) {
        Log.i(TAG, "OnTtsStatusChange :" + TtsRequest.toString())
    }

    override fun onSdkError(sdkException: SdkException) {
        Log.i(TAG, "OnSdkError :" + sdkException.message)
    }

    override fun onWakeupWord(wakeupWord: String, direction: Int) {
        Log.i(TAG,"onWakeWord: " + wakeupWord)
    }

    override fun DialogFlowAgentResponseListener(detectIntentResponse: DetectIntentResponse?) {
        val agentReponse: String? = detectIntentResponse?.queryResult?.fulfillmentText

        if(!agentReponse.isNullOrEmpty()) {
            Log.i(TAG, "DialogFlowAgentReponse :" + agentReponse);
            speak(agentReponse)
        }
        else {
            Log.e(TAG, "DialogFlowAgentResponse : Error, No fulfilment founds" )
        }
    }
}