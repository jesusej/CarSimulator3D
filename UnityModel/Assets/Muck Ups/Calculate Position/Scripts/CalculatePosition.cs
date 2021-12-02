using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CalculatePosition : MonoBehaviour
{
    Vector3 oldPosition;
    Quaternion targetRotation;
    Vector3 targetPosition;
    public float speedRotation = 1;
    public float speedPosition = 1;

    private void Update()
    {
        transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, speedRotation * Time.deltaTime);
        transform.position = Vector3.Lerp(transform.position, targetPosition, Time.deltaTime * speedPosition);
    }

    public void SetPosition(Vector3 position)
    {
        Vector3 direction = oldPosition - position;
        targetRotation = Quaternion.FromToRotation(Vector3.back, direction);
        targetRotation = Quaternion.Euler(0, targetRotation.eulerAngles.y, 0);

        //transform.position = position;
        targetPosition = position;
        oldPosition = position;
    }
}
