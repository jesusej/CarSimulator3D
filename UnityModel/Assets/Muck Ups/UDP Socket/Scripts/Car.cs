using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Car : MonoBehaviour
{
    public int id;
    Vector3 targetPosion;
    public float speed = 1;

    void Update()
    {
        // Con los ejercicios anteriores, buscar la manera de mejorar el smooth de posici�n y giro.
        //
        
            transform.position = Vector3.Lerp(transform.position, targetPosion, Time.deltaTime * speed);
    }

    public void SetTargetPosition(Vector3 position)
    {
        targetPosion = position;
    }
}
