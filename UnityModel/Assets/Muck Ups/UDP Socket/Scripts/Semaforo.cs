using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading;

public class Semaforo : MonoBehaviour
{
    public GameObject luz;

    public Transform posGreen;
    public Transform posRed;
    private bool green;
    private bool red;
    // Start is called before the first frame update
    void Start()
    {
        green = true;
    }

    // Update is called once per frame
    void Update()
    {
            if (green == true) {
                // luz.transform.position = posGreen.position;
                // luz.GetComponent<Light>().color = Color.green;
                StartCoroutine(changeLight());
                
            }
            /*
            if (red == true) {
                luz.transform.position = posRed.position;
                luz.GetComponent<Light>().color = Color.red;
            }
            */
    }

    IEnumerator changeLight() {
        int i = 0;
        while(true) {
            
            // red = true;
            if (i % 2 == 0) {
                luz.transform.position = posGreen.position;
                luz.GetComponent<Light>().color = Color.green;
                
            }
            if (i % 2 == 1)
            {
                luz.transform.position = posRed.position;
                luz.GetComponent<Light>().color = Color.red;
                
            }
            i++;
            yield return new WaitForSeconds(10);
        }
    }

    IEnumerator redLight()
    {
        yield return new WaitForSeconds(3);
        green = true;
    }
}
