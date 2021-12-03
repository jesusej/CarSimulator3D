using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestDriver : MonoBehaviour
{
    public Vector2 minMaxWidth;
    public Vector2 minMaxDepth;
    public float multiplier = 1;
    public float repeatTime = 1;
    public float speedPosition = 1;
    Vector3 targetPosition;
    Vector3 targetRotation;

    enum Directions
    {
        Left,
        Front,
        Right
    }

    struct Option
    {
        public Vector3 position;
        public Directions direction;
        public float rotation;
    }

    void Start()
    {
        InvokeRepeating("Take", 0, repeatTime);
    }
    public float speedRotation;
    private void Update()
    {
        transform.position = Vector3.Lerp(transform.position, targetPosition, Time.deltaTime * speedPosition);
        transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.Euler(targetRotation), Time.deltaTime * speedRotation);
    }
    

    void Take()
    {
        Option[] options = Build(transform);
        if(options.Length < 1)
        {
            return;
        }
        int index = Random.Range(0, options.Length);
        Option option = options[index];

        targetPosition = option.position;
        targetRotation = new Vector3(0, option.rotation + targetRotation.y, 0);

        Debug.Log(option.direction.ToString());
    }

    Option[] Build(Transform t)
    {
        List<Option> options = new List<Option>();
        Vector3[] possiblePositions = new Vector3[] { new Vector3(-1, 0, 0), new Vector3(0, 0, 1), new Vector3(1, 0, 0) };
        float[] possibleRotations = new float[] { -90, 0, 90 };

        for (int i = 0; i < possiblePositions.Length; i++)
        {
            bool isin = true;
            Vector3 nextPosition = t.TransformPoint(possiblePositions[i] * multiplier);
            if (nextPosition.x < minMaxWidth.x || nextPosition.x > minMaxWidth.y)
            {
                isin = false;
            }
            if (nextPosition.z < minMaxDepth.x || nextPosition.z > minMaxDepth.y)
            {
                isin = false;
            }
            if (isin)
            {
                Option o;
                o.direction = (Directions)i;
                o.position = nextPosition;
                o.rotation = possibleRotations[i];
                options.Add(o);
            }
        }

        return options.ToArray();
    }
}
