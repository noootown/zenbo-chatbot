package com.asus.robotdevsample;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.asus.robotframework.API.RobotAPI;
import com.asus.robotframework.API.RobotCallback;
import com.asus.robotframework.API.RobotCmdState;
import com.asus.robotframework.API.RobotErrorCode;
import com.asus.robotframework.API.RobotFace;
import com.asus.robotframework.API.SpeakConfig;

import java.util.*;

import cz.msebera.android.httpclient.Header;
import org.json.*;
import com.loopj.android.http.*;

public class RobotDevSampleActivity extends com.robot.asus.robotactivity.RobotActivity {

    private static RobotAPI mRobotAPI;
    private SpeakConfig s = new SpeakConfig();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.layout_listview_menu);

        //title
        TextView mTextViewTitle = (TextView)findViewById(R.id.textview_title);
        mTextViewTitle.setText(getString(R.string.toolbar_title_mainclass_robotapi_title));
        mRobotAPI = robotAPI;

    }

    @Override
    protected void onResume() {
        super.onResume();
        mRobotAPI.robot.setExpression(RobotFace.HAPPY);
        mRobotAPI.robot.speakAndListen("哈囉，我是 PTT Zenbo，很高興為您服務！", s);
    }

    public RobotDevSampleActivity() {
        super(robotCallback, robotListenCallback);
    }

    public static RobotCallback robotCallback = new RobotCallback() {
        @Override
        public void onResult(int cmd, int serial, RobotErrorCode err_code, Bundle result) {
            super.onResult(cmd, serial, err_code, result);
        }

        @Override
        public void onStateChange(int cmd, int serial, RobotErrorCode err_code, RobotCmdState state) {
            super.onStateChange(cmd, serial, err_code, state);
        }
    };

    public static RobotCallback.Listen robotListenCallback = new RobotCallback.Listen() {
        private String TAG = "voice";
        @Override
        public void onFinishRegister() {
        }

        @Override
        public void onVoiceDetect(JSONObject jsonObject) {
        }

        @Override
        public void onSpeakComplete(String s, String s1) {
        }

        @Override
        public void onEventUserUtterance(JSONObject jsonObject) {
            mRobotAPI.robot.setExpression(RobotFace.HAPPY);
            try {
                List<String> strList = new ArrayList<>();
                JSONArray arr = new JSONArray(jsonObject.getJSONObject("event_user_utterance").get("user_utterance").toString());
                for (int i = 0; i<arr.length(); i++) {
                    JSONArray result = arr.getJSONObject(i).getJSONArray("result");
                    for (int j = 0; j<result.length(); j++) {
                        strList.add(result.getString(j));
                    }
                }
                ChatRestClient.chat(strList.get(0), new JsonHttpResponseHandler() {
                    @Override
                    public void onSuccess(int statusCode, Header[] headers, JSONObject response) {
                        try {
                            SpeakConfig s = new SpeakConfig();
                            s.timeout(20);
                            s.retry(0);
                            mRobotAPI.robot.speakAndListen(response.getString("message"), s);
                        } catch(Exception e) {
                            Log.d(TAG, e.toString());
                        }
                    }
                });
            } catch(Exception e) {
                Log.d(TAG, e.toString());
            }
        }

        @Override
        public void onResult(JSONObject jsonObject) {
        }

        @Override
        public void onRetry(JSONObject jsonObject) {
        }
    };
}
