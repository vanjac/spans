import bpy
import bpy_extras
import bmesh

bl_info = {
    "name": "Export GBA Assembly",
    "author": "chroma zone",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "category": "Import-Export"
}


def mesh_triangulate(mesh):
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()


def export(context, filepath):
    # Exit edit mode before exporting, so current object states are exported properly.
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
    with open(filepath, 'w') as f:
        f.write("\t.section\t.iwram\n")
        f.write("\t.align\t2\n\n")
        
        for obj in context.scene.objects:
            try:
                mesh = obj.to_mesh()
            except RuntimeError:
                continue
            if not mesh:
                continue

            mesh_triangulate(mesh)
            mesh.transform(obj.matrix_world)
            if obj.matrix_world.determinant() < 0.0:
                mesh.flip_normals()

            num_vertices = len(mesh.vertices)
            num_faces = len(mesh.polygons)

            if not (num_vertices + num_faces):
                obj.to_mesh_clear()
                continue

            f.write("\t.global\tpoints_3d\n")
            f.write("points_3d:\n")
            for v in mesh.vertices:
                x = int(round(v.co[0] * 256))
                y = int(round(-v.co[2] * 256))
                z = int(round(v.co[1] * 256))
                f.write("\t.word {0}; .word {1}; .word {2}\n".format(x, y, z))
            
            f.write("\n\t.global\ttransformed_points\n")
            f.write("transformed_points:\n")
            for v in range(0, num_vertices):
                f.write("p{0}:\t.space\t8\n".format(v))

            f.write("\n\t.global\tnum_points\n")
            f.write("num_points:\n")
            f.write("\t.word\t{0}\n\n".format(num_vertices))
            
            f.write("\t.global\ttriangles\n")
            f.write("triangles:\n")
            for face in mesh.polygons:
                fv = face.vertices
                f.write("\t.word p{0}; .word p{1}; .word p{2}\n"
                    .format(fv[0], fv[1], fv[2]))
            f.write("\t.word 0\n")

            obj.to_mesh_clear()  # clean up

            break  # only export one object


class ExportGBA(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):

    bl_idname = "export_scene.gba"
    bl_label = 'Export GBA Assembly'

    # required by ExportHelper
    filename_ext = ".is"
    filter_glob: bpy.props.StringProperty(
        default="*.is",
        options={'HIDDEN'},
        )

    def execute(self, context):
        export(context, self.filepath)
        return {'FINISHED'}

    def draw(self, context):
        pass

def menu_func_export(self, context):
    self.layout.operator(ExportGBA.bl_idname, text="GBA Assembly")


def register():
    bpy.utils.register_class(ExportGBA)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(ExportGBA)


if __name__ == "__main__":
    register()
