using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using System;

public class CustomRequest : MonoBehaviour
{
    public string url = "https://car-sim-chipper-warthog.mybluemix.net/";

    public SpawnManager _spawnManager;
    

    private void Start()
    {
       
        StartCoroutine(GetRequest(url));
    }

    IEnumerator GetRequest(string url)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            // Request and wait for the desired page.
            yield return webRequest.SendWebRequest();
            yield return new WaitForSeconds(2.5f);

            switch (webRequest.result)
            {
                case UnityWebRequest.Result.ConnectionError:
                case UnityWebRequest.Result.DataProcessingError:
                case UnityWebRequest.Result.ProtocolError:
                case UnityWebRequest.Result.Success:
                    string jsonString = webRequest.downloadHandler.text;

                    Debug.Log(":\nReceived: " + jsonString);

                    InfoAgents agent = JsonUtility.FromJson<InfoAgents>(jsonString);
                    
                    _spawnManager.ProcessAgents(agent);
                    break;
            }

            
        }
        
    }
   
}

[Serializable]
public class InfoAgents
{
    public List<InfoCar> Cars;
    public int length;
}

[Serializable]
public class InfoCar
{
    public int CarId;
    public InfoPosition Position;
}

[Serializable]
public class InfoPosition
{
    public float x;
    public float y;
    public float z;
}
