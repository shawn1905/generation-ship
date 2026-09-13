using System;
using System.IO;
using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;

public static class BuildCargo {
    [Serializable] public class Part { public string name, group; public Vector3[] vertices; public int[] triangles; public float[] color; }
    [Serializable] public class Data { public Part[] parts; }
    public static void Run() {
        Directory.CreateDirectory("Assets/Generated");
        var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        var viewer = new GameObject("Cargo viewer").AddComponent<CargoViewer>();
        viewer.variants = new GameObject[2];
        string report = "Native mesh import. Blender (x,y,z) -> Unity (x,z,y); winding reversed.\n";
        for (int i=0; i<2; i++) {
            string label = i==0 ? "L060" : "L080";
            var data = JsonUtility.FromJson<Data>(File.ReadAllText("Assets/Input/"+label+".json"));
            var root = new GameObject(label); viewer.variants[i] = root;
            Bounds all = new Bounds(); bool first = true;
            foreach (var p in data.parts) {
                var go = new GameObject(p.name); go.transform.parent = root.transform;
                var mesh = new Mesh { name = p.name, indexFormat = UnityEngine.Rendering.IndexFormat.UInt32 };
                mesh.vertices = p.vertices; mesh.triangles = p.triangles; mesh.RecalculateNormals(); mesh.RecalculateBounds();
                AssetDatabase.CreateAsset(mesh,"Assets/Generated/"+label+"_"+p.name+".asset");
                go.AddComponent<MeshFilter>().sharedMesh = mesh;
                var material = new Material(Shader.Find("Standard"));
                material.color = new Color(p.color[0],p.color[1],p.color[2],1);
                material.SetFloat("_Metallic", .35f); material.SetFloat("_Glossiness", .4f);
                AssetDatabase.CreateAsset(material,"Assets/Generated/"+label+"_"+p.name+".mat");
                var renderer = go.AddComponent<MeshRenderer>(); renderer.sharedMaterial = material;
                go.AddComponent<CargoPart>().group = p.group;
                if (first) { all = renderer.bounds; first=false; } else all.Encapsulate(renderer.bounds);
            }
            float expected = i==0 ? .66f : .86f;
            if (Mathf.Abs(all.size.x-expected)>.0001f || Mathf.Abs(all.size.y-.427f)>.0001f || Mathf.Abs(all.size.z-.53f)>.0001f)
                throw new Exception("Unit/axis bounds mismatch: "+all.size);
            report += label+": "+data.parts.Length+" parts; bounds metres "+all.size.ToString("F6")+" PASS\n";
        }
        var camera = new GameObject("Inspection camera").AddComponent<Camera>();
        camera.transform.position = new Vector3(.9f,.8f,-1.2f); camera.transform.LookAt(new Vector3(0,.25f,0));
        camera.clearFlags=CameraClearFlags.SolidColor; camera.backgroundColor=new Color(.10f,.12f,.15f);
        camera.nearClipPlane=.01f; camera.farClipPlane=30; viewer.viewCamera=camera;
        var light = new GameObject("Key light").AddComponent<Light>(); light.type=LightType.Directional;
        light.intensity=1.5f; light.transform.rotation=Quaternion.Euler(45,-35,0);
        RenderSettings.ambientLight=new Color(.5f,.5f,.5f);
        // Reference ruler is outside the model; actual length exactly 1 metre.
        var ruler=GameObject.CreatePrimitive(PrimitiveType.Cube); ruler.name="REFERENCE_1_METRE";
        ruler.transform.localScale=new Vector3(1,.006f,.012f); ruler.transform.position=new Vector3(0,-.01f,-.36f);
        viewer.SelectVariant(0); viewer.SetExploded(true);
        foreach (Transform p in viewer.variants[0].transform)
            if (p.GetComponent<CargoPart>().group=="lid" && Mathf.Abs(p.localPosition.y-.30f)>.0001f) throw new Exception("Explosion state failed");
        viewer.SetExploded(false); viewer.SelectVariant(1);
        if (viewer.variants[0].activeSelf || !viewer.variants[1].activeSelf) throw new Exception("Variant selection failed");
        viewer.SelectVariant(0);
        report += "Explosion/reset and variant selection methods PASS; interactive mouse/keyboard not automatically exercised.\n";
        EditorSceneManager.SaveScene(scene,"Assets/CargoInspection.unity");
        AssetDatabase.SaveAssets();
        File.WriteAllText("import-verification.txt",report);
        Debug.Log(report);
    }
}
