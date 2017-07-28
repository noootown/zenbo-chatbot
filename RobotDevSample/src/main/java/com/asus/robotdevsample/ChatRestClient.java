package com.asus.robotdevsample;
import com.loopj.android.http.*;

public class ChatRestClient {
    private static final String BASE_URL = Config.BASE_URL;

    private static AsyncHttpClient client = new AsyncHttpClient();

    public static void get(String url, RequestParams params, AsyncHttpResponseHandler responseHandler) {
        client.get(getAbsoluteUrl(url), params, responseHandler);
    }

    public static void post(String url, RequestParams params, AsyncHttpResponseHandler responseHandler) {
        client.post(getAbsoluteUrl(url), params, responseHandler);
    }

    public static void chat(String msg, AsyncHttpResponseHandler responseHandler) {
        RequestParams params = new RequestParams();
        params.put("msg", msg);
        client.get(getAbsoluteUrl("chat"), params, responseHandler);
    }

    private static String getAbsoluteUrl(String relativeUrl) {
        return BASE_URL + relativeUrl;
    }
}
