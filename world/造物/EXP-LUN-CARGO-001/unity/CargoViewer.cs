using UnityEngine;

public class CargoViewer : MonoBehaviour {
    public GameObject[] variants;
    public Camera viewCamera;
    bool exploded;
    int variant;
    float yaw = -40, pitch = 28, distance = 1.5f;
    public void SetExploded(bool value) {
        exploded = value;
        foreach (var root in variants) foreach (Transform part in root.transform) {
            var tag = part.GetComponent<CargoPart>();
            var offset = Vector3.zero;
            if (tag.group == "lid") offset.y = .30f;
            if (tag.group == "liner") offset.y = .14f;
            if (tag.group == "base") offset.y = -.12f;
            if (tag.group == "lid_lock" || tag.group == "dock_lock")
                offset.x = Mathf.Sign(part.GetComponent<MeshRenderer>().localBounds.center.x) * .09f;
            part.localPosition = offset * (value ? 1 : 0);
        }
    }
    public void SelectVariant(int index) {
        variant = index;
        for (int i = 0; i < variants.Length; i++) variants[i].SetActive(i == index);
    }
    void Update() {
        if (Input.GetMouseButton(0) && Input.mousePosition.y < Screen.height - 105) {
            yaw += Input.GetAxis("Mouse X") * 4;
            pitch = Mathf.Clamp(pitch - Input.GetAxis("Mouse Y") * 3, -10, 85);
        }
        distance = Mathf.Clamp(distance - Input.mouseScrollDelta.y * .10f, .65f, 3);
        if (Input.GetKeyDown(KeyCode.Space)) SetExploded(!exploded);
        if (Input.GetKeyDown(KeyCode.Alpha1)) SelectVariant(0);
        if (Input.GetKeyDown(KeyCode.Alpha2)) SelectVariant(1);
        var target = new Vector3(0,.28f,0);
        viewCamera.transform.position = target + Quaternion.Euler(pitch,yaw,0) * new Vector3(0,0,-distance);
        viewCamera.transform.LookAt(target);
    }
    void OnGUI() {
        GUI.Box(new Rect(15,15,560,85), "EXP-LUN-CARGO-001  /  ENGINEERING GEOMETRY STUDY");
        if (GUI.Button(new Rect(25,45,100,28),"600 mm")) SelectVariant(0);
        if (GUI.Button(new Rect(135,45,100,28),"800 mm")) SelectVariant(1);
        if (GUI.Button(new Rect(245,45,130,28),exploded ? "Assemble [Space]" : "Explode [Space]")) SetExploded(!exploded);
        GUI.Label(new Rect(25,78,550,25),"Drag to orbit | Scroll to zoom | 1/2: variant | Not load-certified");
    }
}
