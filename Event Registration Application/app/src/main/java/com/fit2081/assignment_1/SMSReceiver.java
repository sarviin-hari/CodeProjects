package com.fit2081.assignment_1;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.provider.Telephony;
import android.telephony.SmsMessage;
import android.widget.Toast;

public class SMSReceiver extends BroadcastReceiver {

    public static final String SMS_FILTER = "SMS_FILTER";
    public static final String SMS_MSG_KEY = "SMS_MSG_KEY";

    /*
     * This method 'onReceive' will be invoked with each new incoming SMS
     * */
    @Override
    public void onReceive(Context context, Intent intent) {
        // TODO: This method is called when the BroadcastReceiver is receiving
        // an Intent broadcast.
//        throw new UnsupportedOperationException("Not yet implemented");
        /*
         * Use the Telephony class to extract the incoming messages from the intent
         * Can do without for loop
         * */
        SmsMessage[] messages = Telephony.Sms.Intents.getMessagesFromIntent(intent);
        for (int i = 0; i < messages.length; i++) {
            SmsMessage currentMessage = messages[i];
            String message = currentMessage.getDisplayMessageBody();

//            if (message.length() >= 9 && (message.substring(0,9)).equals("category:")){
//                Intent msgIntent = new Intent();
//                msgIntent.setAction(SMS_FILTER2);
//                msgIntent.putExtra(SMS_MSG_KEY2, message);
//                context.sendBroadcast(msgIntent);
//            }
//            else if (message.length() >= 6 && (message.substring(0,6)).equals("event:")){
//                Intent msgIntent = new Intent();
//                msgIntent.setAction(SMS_FILTER);
//                msgIntent.putExtra(SMS_MSG_KEY, message);
//                context.sendBroadcast(msgIntent);
//            }
//            else{
//                Toast.makeText(context, "Wrong message format!", Toast.LENGTH_SHORT).show();
//            }



            Intent msgIntent = new Intent();
            msgIntent.setAction(SMS_FILTER);
            msgIntent.putExtra(SMS_MSG_KEY, message);
            context.sendBroadcast(msgIntent);
        }
    }
}
