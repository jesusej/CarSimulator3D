using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarManager : MonoBehaviour
{
    IPositionProvider provider;
    public Transform target;

    public float repeatingTime = 1;
    public float timeMultiplier = 1;

    public CalculatePosition calculatePosition;

    void Start()
    {
        provider = new PositionMuckUp();
        InvokeRepeating("ReadPosition", 1, repeatingTime);
    }

    void ReadPosition()
    {
        Vector3 position = provider.GetPosition(Time.time * timeMultiplier);
        calculatePosition.SetPosition(position);
    }
}

public interface IPositionProvider
{
    Vector3 GetPosition(float time);
}

public class PositionMuckUp : IPositionProvider
{
    public Vector3[] positions = new Vector3[] {
        new Vector3(0,0,0),
        new Vector3(5,0,0),
        new Vector3(10,0,0),
        new Vector3(15,0,0),
        new Vector3(20,0,0),
        new Vector3(20,0,5),
        new Vector3(20,0,10),
        new Vector3(20,0,15),
        new Vector3(20,0,20)
    };

    public Vector3 GetPosition(float time)
    {
        int index = (int)Mathf.PingPong(time, positions.Length);
        return positions[index];
    }
}