using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpawnManager : MonoBehaviour
{
    public GameObject carPrefab;
    InfoAgents _agents;
    List<Car> sceneCars = new List<Car>();
    public float wait = 2;
    public int actual = 0;

    public void ProcessAgents(InfoAgents agents) {
        
        StartCoroutine(Animate(agents));
    }

    IEnumerator Animate(InfoAgents agents) {
        int steps = (agents.Cars.Count) / agents.length;
        
         for (int i = 0; i < steps; i++){
            UpdateAgents(agents);
            yield return new WaitForSeconds(wait);     
         }
        
    }

    public void UpdateAgents(InfoAgents agents)
    {
        // Esto se ejecutaria una s�la vez.
        if(_agents == null)
        {
            Debug.Log(agents.Cars.Count);
            for (int i = 0; i < agents.length; i++)
            {
                Car car = Instantiate(carPrefab).GetComponent<Car>();
                car.id = agents.Cars[i].CarId;
                car.transform.position = new Vector3(agents.Cars[i].Position.x * 5, 0, agents.Cars[i].Position.z * 5);
            
                sceneCars.Add(car);

            }
        }

        _agents = agents;

        // Ejemplo de buscar por id.
         
        for (int i = 0; i < agents.length; i++)
        {
            // Poner atenci�n en la interpretaci�n del orden de las coordenadas de python (X,Y) y de Unity (X,Y,Z),
            // porque la profundidad en Python es en el eje Y y en Unity ser�a Z � a sus criterios.
            Vector3 newPosition = new Vector3(agents.Cars[actual].Position.x * 5, 0, agents.Cars[i + actual].Position.z * 5);
            // Console.Log("Position: ",newPosition);
            // Para buscar por id.
            Car car = sceneCars.Find(s => s.id == agents.Cars[actual].CarId);
            car.SetTargetPosition(newPosition);
            actual++;
        }
        
    }
}
